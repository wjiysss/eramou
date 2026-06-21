"""LLM 网页界面服务器

提供独立的 HTTP 服务器承载 LLM 聊天界面。
启动: python -m eraMaouEx_modules.llm.web  或  Start_LLM_Web.bat
端口: 127.0.0.1:4315
"""
from __future__ import annotations
import json
import sys
import threading
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Optional

from .config import load_config, load_embedding_config
from .client import LLMClient, LLMError
from .context import ContextBuilder
from .skills import SkillRegistry
from .context_manager import ContextManager
from .embedding import EmbeddingClient
from .rag import RAGSystem
from .erb_knowledge import build_static_knowledge

HOST = "127.0.0.1"
PORT = 4315


class GameRuntime:
    def __init__(self):
        self.engine = None
        self.client: Optional[LLMClient] = None
        self.context: Optional[ContextBuilder] = None
        self.skills: Optional[SkillRegistry] = None
        self.embedder: Optional[EmbeddingClient] = None
        self.rag: Optional[RAGSystem] = None
        self.context_manager: Optional[ContextManager] = None
        self.messages: list[dict[str, Any]] = []
        self.current_state = "START"
        self.started = False
        self.start_greeting: Optional[str] = None
        self.lock = threading.Lock()
        self.init_error: Optional[str] = None

    def initialize(self, erb_dir: str) -> None:
        from eraMaouEx import GameEngine, Character

        config = load_config(silent=True)
        if config is None:
            self.init_error = (
                "未找到 ERAMOU_LLM_API_KEY。请在项目根目录创建 .env 文件（参考 .env.example），"
                "或设置环境变量后重启。"
            )
            return

        try:
            engine = GameEngine(erb_dir)
            engine._bootstrap_game_runtime()
            engine._system_init()
            if not engine.interpreter.vars.chars:
                master = None
                try:
                    master = engine._create_character_from_template(0)
                except Exception as e:
                    print(f"[LLM Web] master 模板加载失败，回退手动构造: {e}")
                if master is None:
                    from eraMaouEx import Character as _Char
                    master = _Char()
                    master.name = "你"
                    master.callname = "你"
                    master.base[0] = 10000; master.maxbase[0] = 10000
                    master.base[1] = 10000; master.maxbase[1] = 10000
                    engine.interpreter.vars.chars.append(master)
                # 兜底默认魔王设定（玩家可通过 START 第一步的 configure_master 工具覆盖）
                chars = engine.interpreter.vars.chars
                chars[0].name = chars[0].name or "你"
                if not chars[0].callname:
                    chars[0].callname = chars[0].name
                chars[0].talent[200] = 1  # 魔王标签
                if not chars[0].cflag.get(451):
                    chars[0].cflag[451] = 21
            self.engine = engine
            self.client = LLMClient(config)
            # RAG：尝试加载 embedding 配置；缺失时优雅降级（不注入相关知识）
            emb_config = load_embedding_config(silent=True)
            if emb_config is not None:
                try:
                    self.embedder = EmbeddingClient(emb_config)
                    index_dir = os.path.join(os.path.dirname(erb_dir), ".trae", "rag_index")
                    self.rag = RAGSystem(self.embedder, index_dir)
                    self.rag.load_events()
                    static_items = build_static_knowledge(erb_dir)
                    self.rag.build_static_if_needed(static_items)
                    print(f"[LLM Web] RAG 就绪：static={len(self.rag.static_index.entries)} events={len(self.rag.event_index.entries)}")
                except Exception as e:
                    print(f"[LLM Web] RAG 初始化失败，降级为不注入: {e}")
                    self.embedder = None
                    self.rag = None
            else:
                print("[LLM Web] 未配置 embedding，RAG 检索禁用（游戏可正常运行）")
            self.context = ContextBuilder(engine, rag=self.rag)
            self.skills = SkillRegistry(engine, self.context, rag=self.rag, runtime=self)
            self.context_manager = ContextManager()
            self.messages = [{"role": "system", "content": self.context.build_start_prompt()}]
        except Exception as e:
            self.init_error = f"游戏引擎初始化失败: {e}"

    def chat(self, user_input: str) -> dict[str, Any]:
        if self.init_error:
            return {"reply": f"[初始化错误] {self.init_error}", "tool_calls": [], "state": "", "error": True}
        if self.client is None or self.skills is None or self.context is None:
            return {"reply": "[错误] 服务未就绪", "tool_calls": [], "state": "", "error": True}

        with self.lock:
            # __start__ 是前端触发的开场白请求，转为最小提示让 LLM 主动开口
            if user_input == "__start__":
                effective_input = "(请开始你的开场白)"
                retrieval_query = ""  # 合成输入不参与 RAG 检索
            else:
                effective_input = user_input
                retrieval_query = user_input
            self.messages.append({"role": "user", "content": effective_input})
            tools = self.skills.tool_schemas()
            tool_log: list[dict[str, Any]] = []
            reply_text = ""
            MAX_TOOL_ROUNDS = 5

            for round_idx in range(MAX_TOOL_ROUNDS):
                if self.current_state == "START":
                    sys_prompt = self.context.build_start_prompt()
                else:
                    sys_prompt = self.context.build_system_prompt(self.current_state, user_query=retrieval_query)
                self.messages[0] = {"role": "system", "content": sys_prompt}
                try:
                    result = self.client.chat(self.messages, tools=tools)
                except LLMError as e:
                    self.messages.pop()
                    return {"reply": f"[LLM 错误] {e}", "tool_calls": tool_log, "state": self._state_text(), "error": True}
                except Exception as e:
                    self.messages.pop()
                    return {"reply": f"[未知错误] {e}", "tool_calls": tool_log, "state": self._state_text(), "error": True}

                if result.content:
                    self.messages.append({"role": "assistant", "content": result.content})

                if not result.tool_calls:
                    reply_text = result.content or "(无回应)"
                    break

                assistant_msg: dict[str, Any] = {"role": "assistant", "content": result.content or ""}
                assistant_msg["tool_calls"] = [
                    {"id": tc.id, "type": "function", "function": {"name": tc.name, "arguments": tc.arguments}}
                    for tc in result.tool_calls
                ]
                if self.messages and self.messages[-1].get("role") == "assistant" and "tool_calls" not in self.messages[-1]:
                    self.messages[-1] = assistant_msg
                else:
                    self.messages.append(assistant_msg)
                if not result.content:
                    reply_text = ""

                for tc in result.tool_calls:
                    args = tc.parsed_args()
                    tool_result = self.skills.dispatch(tc.name, args)
                    self._apply_state_change(tc.name, args, tool_result)
                    tool_log.append({"name": tc.name, "args": args, "result": tool_result[:300]})
                    self.messages.append({"role": "tool", "tool_call_id": tc.id, "name": tc.name, "content": tool_result})
            else:
                reply_text = "(工具调用轮次已达上限，请继续输入下一条指令。)"

            # 上下文管理：用 ContextManager 替代旧的「>22 条硬裁剪」
            # 保证 tool_call/tool_result 配对完整，超预算时优先摘要压缩，失败降级配对裁剪
            if self.context_manager is not None:
                try:
                    self.messages = self.context_manager.manage(self.messages, llm_client=self.client)
                except Exception as e:
                    print(f"[LLM Web] 上下文管理失败，保留原消息: {e}")
            else:
                if len(self.messages) > 22:
                    self.messages = [self.messages[0]] + self.messages[-21:]

            return {
                "reply": reply_text,
                "tool_calls": tool_log,
                "state": self._state_text(),
                "error": False,
            }

    def chat_stream(self, user_input: str):
        if self.init_error:
            yield {"type": "error", "message": f"[初始化错误] {self.init_error}"}
            return
        if self.client is None or self.skills is None or self.context is None:
            yield {"type": "error", "message": "[错误] 服务未就绪"}
            return

        with self.lock:
            if user_input == "__start__":
                effective_input = "(请开始你的开场白)"
                retrieval_query = ""
            else:
                effective_input = user_input
                retrieval_query = user_input
            self.messages.append({"role": "user", "content": effective_input})
            tools = self.skills.tool_schemas()
            MAX_TOOL_ROUNDS = 5

            for round_idx in range(MAX_TOOL_ROUNDS):
                if self.current_state == "START":
                    sys_prompt = self.context.build_start_prompt()
                else:
                    sys_prompt = self.context.build_system_prompt(self.current_state, user_query=retrieval_query)
                self.messages[0] = {"role": "system", "content": sys_prompt}

                full_content: list[str] = []
                final_tool_calls: list = []
                try:
                    for ev in self.client.chat_stream(self.messages, tools=tools):
                        et = ev.get("type")
                        if et == "content_delta":
                            full_content.append(ev["content"])
                            yield {"type": "token", "text": ev["content"]}
                        elif et == "tool_calls_done":
                            final_tool_calls = ev.get("tool_calls") or []
                        elif et == "done":
                            if ev.get("tool_calls"):
                                final_tool_calls = ev["tool_calls"]
                except LLMError as e:
                    self.messages.pop()
                    yield {"type": "error", "message": f"[LLM 错误] {e}"}
                    return
                except Exception as e:
                    self.messages.pop()
                    yield {"type": "error", "message": f"[未知错误] {e}"}
                    return

                content = "".join(full_content)
                if content:
                    self.messages.append({"role": "assistant", "content": content})

                if not final_tool_calls:
                    break

                assistant_msg: dict[str, Any] = {"role": "assistant", "content": content or ""}
                assistant_msg["tool_calls"] = [
                    {"id": tc.id, "type": "function", "function": {"name": tc.name, "arguments": tc.arguments}}
                    for tc in final_tool_calls
                ]
                if self.messages and self.messages[-1].get("role") == "assistant" and "tool_calls" not in self.messages[-1]:
                    self.messages[-1] = assistant_msg
                else:
                    self.messages.append(assistant_msg)

                for tc in final_tool_calls:
                    args = tc.parsed_args()
                    tool_result = self.skills.dispatch(tc.name, args)
                    self._apply_state_change(tc.name, args, tool_result)
                    yield {"type": "tool", "name": tc.name, "args": args, "result": tool_result[:300]}
                    self.messages.append({"role": "tool", "tool_call_id": tc.id, "name": tc.name, "content": tool_result})
            else:
                yield {"type": "token", "text": "(工具调用轮次已达上限，请继续输入下一条指令。)"}

            if self.context_manager is not None:
                try:
                    self.messages = self.context_manager.manage(self.messages, llm_client=self.client)
                except Exception as e:
                    print(f"[LLM Web] 上下文管理失败，保留原消息: {e}")
            else:
                if len(self.messages) > 22:
                    self.messages = [self.messages[0]] + self.messages[-21:]

            yield {"type": "done", "state": self._state_text()}

    def _state_text(self) -> str:
        if self.engine is None or self.context is None:
            return ""
        s = self.engine.state
        time_str = "上午" if s.time == 0 else "下午"
        return f"第{s.day[2]}天 {time_str} | 金钱:{s.money} | 状态:{self.current_state}"

    def _apply_state_change(self, tool_name: str, args: dict[str, Any], tool_result: str) -> None:
        if tool_name in ("create_character", "random_character") and tool_result.startswith("已创建角色"):
            self.current_state = "SHOP"
            self.started = True
            try:
                if self.context is not None and self.context._try_auto_lock_target():
                    target_no = self.engine.state.target_no
                    chars = self.engine.interpreter.vars.chars
                    if 0 <= target_no < len(chars):
                        name = getattr(chars[target_no], "name", "调教对象")
                        print(f"[LLM Web] 唯一调教对象自动锁定: {name}")
            except Exception as e:
                print(f"[LLM Web] 自动锁定失败（不影响流程）: {e}")
        elif tool_name == "select_target" and tool_result.startswith("已选择"):
            self.current_state = "TRAIN"
        elif tool_name == "advance_time":
            self.current_state = "SHOP"


RUNTIME = GameRuntime()


PAGE_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>eraMaouEx - LLM 驱动模式</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, "Segoe UI", "Microsoft YaHei", sans-serif;
    background: linear-gradient(135deg, #1a0f2e 0%, #2d1b4e 50%, #1a0f2e 100%);
    color: #e6d8ff;
    height: 100vh;
    display: flex;
    flex-direction: column;
  }
  header {
    background: rgba(0,0,0,0.4);
    padding: 12px 20px;
    border-bottom: 1px solid #4a2c7a;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
  }
  header h1 { font-size: 18px; color: #c8a4ff; }
  #status-bar {
    font-size: 13px;
    color: #9d7fd1;
    background: rgba(74,44,122,0.3);
    padding: 6px 14px;
    border-radius: 14px;
  }
  #chat {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .msg {
    max-width: 80%;
    padding: 12px 16px;
    border-radius: 14px;
    line-height: 1.6;
    white-space: pre-wrap;
    word-wrap: break-word;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  }
  .msg.user {
    align-self: flex-end;
    background: linear-gradient(135deg, #6b3fa0, #8b5fbf);
    color: white;
    border-bottom-right-radius: 4px;
  }
  .msg.gm {
    align-self: flex-start;
    background: rgba(40,25,70,0.85);
    border: 1px solid #4a2c7a;
    border-bottom-left-radius: 4px;
  }
  .msg.system {
    align-self: center;
    background: rgba(255,200,100,0.15);
    border: 1px solid rgba(255,200,100,0.4);
    color: #ffd485;
    font-size: 13px;
    max-width: 90%;
  }
  .tools {
    align-self: flex-start;
    max-width: 80%;
    background: rgba(0,180,160,0.1);
    border-left: 3px solid #00b4a0;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 12px;
    color: #7fe8da;
    margin-top: -8px;
  }
  .tools summary { cursor: pointer; color: #4dd6c2; font-weight: 600; }
  .tools .entry { margin-top: 6px; padding: 4px 0; border-top: 1px dashed rgba(0,180,160,0.3); }
  .tools .entry:first-of-type { border-top: none; }
  .tools .name { color: #4dd6c2; font-weight: 600; }
  .tools pre { margin-top: 4px; white-space: pre-wrap; font-size: 11px; color: #a8d8ce; }
  footer {
    background: rgba(0,0,0,0.4);
    padding: 14px 20px;
    border-top: 1px solid #4a2c7a;
    display: flex;
    gap: 10px;
  }
  #input {
    flex: 1;
    background: rgba(30,18,55,0.8);
    border: 1px solid #4a2c7a;
    color: #e6d8ff;
    padding: 12px 16px;
    border-radius: 10px;
    font-size: 14px;
    outline: none;
    transition: border-color 0.2s;
  }
  #input:focus { border-color: #8b5fbf; }
  #input:disabled { opacity: 0.5; cursor: not-allowed; }
  #send {
    background: linear-gradient(135deg, #6b3fa0, #8b5fbf);
    color: white;
    border: none;
    padding: 0 24px;
    border-radius: 10px;
    font-size: 14px;
    cursor: pointer;
    font-weight: 600;
    transition: opacity 0.2s;
  }
  #send:hover:not(:disabled) { opacity: 0.9; }
  #send:disabled { opacity: 0.4; cursor: not-allowed; }
  #chat::-webkit-scrollbar { width: 8px; }
  #chat::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); }
  #chat::-webkit-scrollbar-thumb { background: #4a2c7a; border-radius: 4px; }
  .typing { color: #9d7fd1; font-style: italic; }
</style>
</head>
<body>
<header>
  <h1>eraMaouEx - LLM 驱动模式</h1>
  <div id="status-bar">加载中...</div>
</header>
<div id="chat"></div>
<footer>
  <input id="input" type="text" placeholder="用自然语言描述你想做的事（如：查询状态 / 购买道具0 / 选择调教对象）" autocomplete="off" disabled>
  <button id="send" disabled>发送</button>
</footer>
<script>
const chat = document.getElementById('chat');
const input = document.getElementById('input');
const sendBtn = document.getElementById('send');
const statusBar = document.getElementById('status-bar');

function addMsg(text, cls) {
  const div = document.createElement('div');
  div.className = 'msg ' + cls;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

function addTools(tools) {
  if (!tools || tools.length === 0) return;
  const wrap = document.createElement('details');
  wrap.className = 'tools';
  wrap.innerHTML = '<summary>工具调用 (' + tools.length + ')</summary>';
  tools.forEach(t => {
    const entry = document.createElement('div');
    entry.className = 'entry';
    const argsStr = JSON.stringify(t.args);
    entry.innerHTML = '<span class="name">' + t.name + '</span>(' + argsStr + ')';
    const pre = document.createElement('pre');
    pre.textContent = t.result;
    entry.appendChild(pre);
    wrap.appendChild(entry);
  });
  chat.appendChild(wrap);
  chat.scrollTop = chat.scrollHeight;
}

function setStatus(text) { statusBar.textContent = text; }

function setBusy(busy) {
  input.disabled = busy;
  sendBtn.disabled = busy;
  if (!busy) input.focus();
}

async function streamChat(message, bubble) {
  const resp = await fetch('/api/chat/stream', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: message})
  });
  const reader = resp.body.getReader();
  const decoder = new TextDecoder('utf-8');
  let buffer = '';
  let gm = null;
  const reuseBubble = () => {
    if (bubble && bubble.className.indexOf('typing') >= 0) {
      bubble.className = 'gm';
      return bubble;
    }
    return addMsg('', 'gm');
  };
  while (true) {
    const {done, value} = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, {stream: true});
    let idx;
    while ((idx = buffer.indexOf('\\n\\n')) >= 0) {
      const eventStr = buffer.slice(0, idx);
      buffer = buffer.slice(idx + 2);
      const lines = eventStr.split('\\n');
      for (const line of lines) {
        if (!line.startsWith('data:')) continue;
        const jsonStr = line.slice(5).trim();
        if (!jsonStr) continue;
        let ev;
        try { ev = JSON.parse(jsonStr); } catch (e) { continue; }
        if (ev.type === 'token') {
          if (!gm) gm = reuseBubble();
          gm.textContent += ev.text;
          chat.scrollTop = chat.scrollHeight;
        } else if (ev.type === 'tool') {
          addTools([{name: ev.name, args: ev.args, result: ev.result}]);
        } else if (ev.type === 'done') {
          setStatus(ev.state || '');
          if (!gm) {
            const b = reuseBubble();
            b.textContent = '(无回应)';
          }
          setBusy(false);
          return;
        } else if (ev.type === 'error') {
          if (!gm) {
            const b = reuseBubble();
            b.className = 'msg system';
            b.textContent = ev.message;
          } else {
            gm.textContent += '\\n[错误] ' + ev.message;
          }
          setBusy(false);
          return;
        }
      }
    }
  }
  if (!gm) {
    const b = reuseBubble();
    b.className = 'msg system';
    b.textContent = '(连接中断)';
  }
  setBusy(false);
}

async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;
  input.value = '';
  addMsg(text, 'user');
  setBusy(true);
  const typing = addMsg('GM 思考中...', 'gm typing');
  try {
    await streamChat(text, typing);
  } catch (e) {
    if (typing.className.indexOf('typing') >= 0) typing.remove();
    addMsg('请求失败: ' + e.message, 'system');
    setBusy(false);
  }
}

sendBtn.addEventListener('click', sendMessage);
input.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

(async function init() {
  try {
    const resp = await fetch('/api/state');
    const data = await resp.json();
    if (data.error) {
      addMsg(data.message, 'system');
      return;
    }
    setStatus(data.state || '');
    addMsg('【游戏开始】正在准备魔界...请稍候，GM 将引导你创建角色。', 'system');
    setBusy(true);
    const typing = addMsg('GM 思考中...', 'gm typing');
    try {
      await streamChat('__start__', typing);
    } catch (e) {
      if (typing.className.indexOf('typing') >= 0) typing.remove();
      addMsg('初始化失败: ' + e.message, 'system');
      setBusy(false);
    }
  } catch (e) {
    addMsg('初始化失败: ' + e.message, 'system');
    setBusy(false);
  }
})();
</script>
</body>
</html>
"""


class LLMHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/" or path == "":
            self._send_html(PAGE_HTML)
            return
        if path == "/api/state":
            if RUNTIME.init_error:
                self._send_json({"error": True, "message": RUNTIME.init_error})
            else:
                self._send_json({"error": False, "state": RUNTIME._state_text()})
            return
        self.send_error(404)

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        if path == "/api/chat/stream":
            length = int(self.headers.get("Content-Length", "0") or 0)
            try:
                payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
                return
            message = str(payload.get("message", "")).strip()
            if not message:
                self._handle_chat_stream_error("消息不能为空")
                return
            self._handle_chat_stream(message)
            return
        if path != "/api/chat":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0") or 0)
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return
        message = str(payload.get("message", "")).strip()
        if not message:
            self._send_json({"reply": "消息不能为空", "tool_calls": [], "state": RUNTIME._state_text(), "error": True})
            return
        result = RUNTIME.chat(message)
        self._send_json(result)

    def _handle_chat_stream(self, message):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "keep-alive")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()
        try:
            for ev in RUNTIME.chat_stream(message):
                line = "data: " + json.dumps(ev, ensure_ascii=False) + "\n\n"
                self.wfile.write(line.encode("utf-8"))
                self.wfile.flush()
        except Exception as e:
            err = "data: " + json.dumps({"type": "error", "message": str(e)}, ensure_ascii=False) + "\n\n"
            try:
                self.wfile.write(err.encode("utf-8"))
                self.wfile.flush()
            except Exception:
                pass

    def _handle_chat_stream_error(self, message):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "keep-alive")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()
        try:
            err = "data: " + json.dumps({"type": "error", "message": message}, ensure_ascii=False) + "\n\n"
            self.wfile.write(err.encode("utf-8"))
            self.wfile.flush()
        except Exception:
            pass

    def _send_json(self, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html):
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


def _resolve_erb_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(here))


def main():
    erb_dir = _resolve_erb_dir()
    game_dir = r"F:\code\eraMaouEx"
    if os.path.exists(game_dir):
        erb_dir = game_dir

    print(f"Game directory: {erb_dir}")
    print("[LLM Web] 初始化游戏引擎...")
    RUNTIME.initialize(erb_dir)

    if RUNTIME.init_error:
        print(f"[LLM Web] 初始化失败: {RUNTIME.init_error}")
        print("[LLM Web] 服务仍将启动以便显示错误页，但聊天功能不可用。")
    else:
        print(f"[LLM Web] 就绪。模型: {RUNTIME.client.config.model}")

    server = ThreadingHTTPServer((HOST, PORT), LLMHandler)
    print(f"[LLM Web] 服务地址: http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[LLM Web] 停止服务。")


if __name__ == "__main__":
    main()
