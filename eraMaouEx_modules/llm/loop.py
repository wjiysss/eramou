"""LLM 游戏循环

用户输入 → 构建 RAG 上下文 → 调用 LLM → 处理工具调用 → 输出回应 → 等待输入
"""
from __future__ import annotations
import json
from typing import TYPE_CHECKING, Any

from .client import LLMClient, LLMError
from .context import ContextBuilder
from .skills import SkillRegistry

if TYPE_CHECKING:
    from eraMaouEx import GameEngine


EXIT_TOKENS = {"quit", "exit", "退出", ":q", "q", "bye", "再见"}
MAX_TOOL_ROUNDS = 5
MAX_HISTORY_MESSAGES = 20


class LLMGameLoop:
    def __init__(
        self,
        engine: "GameEngine",
        client: LLMClient,
        context_builder: ContextBuilder,
        skill_registry: SkillRegistry,
    ):
        self.engine = engine
        self.client = client
        self.context = context_builder
        self.skills = skill_registry
        self.current_state = "SHOP"
        self.messages: list[dict[str, Any]] = []
        self.running = True

    def run(self) -> None:
        print("=" * 60)
        print("  eraMaouEx - LLM 驱动模式")
        print(f"  模型: {self.client.config.model}")
        print("  输入 '退出' / 'quit' 结束。用自然语言描述你想做的事。")
        print("=" * 60)

        self.messages = []
        self.messages.append({"role": "system", "content": self._build_system()})

        while self.running:
            try:
                user_input = input("\n[魔王] > ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n再见。")
                break

            if not user_input:
                continue
            if user_input.lower() in EXIT_TOKENS:
                print("游戏结束。再见。")
                break

            self._process_turn(user_input)

    def _build_system(self) -> str:
        return self.context.build_system_prompt(self.current_state)

    def _process_turn(self, user_input: str) -> None:
        self.messages.append({"role": "user", "content": user_input})
        tools = self.skills.tool_schemas()

        for round_idx in range(MAX_TOOL_ROUNDS):
            # 每轮刷新系统提示(反映最新状态)
            self.messages[0] = {"role": "system", "content": self._build_system()}

            try:
                result = self.client.chat(self.messages, tools=tools)
            except LLMError as e:
                print(f"[LLM 错误] {e}")
                self.messages.pop()
                return
            except Exception as e:
                print(f"[未知错误] {e}")
                self.messages.pop()
                return

            if result.content:
                self.messages.append({"role": "assistant", "content": result.content})

            if not result.tool_calls:
                if result.content:
                    print(f"\n[GM] {result.content}")
                else:
                    print("[GM] (无回应)")
                break

            # 有工具调用：构造 assistant 消息(含 tool_calls)
            assistant_msg: dict[str, Any] = {"role": "assistant", "content": result.content or ""}
            assistant_msg["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.name, "arguments": tc.arguments},
                }
                for tc in result.tool_calls
            ]
            # 替换最后一条纯 content 的 assistant 消息为带 tool_calls 的版本
            if self.messages and self.messages[-1].get("role") == "assistant" and "tool_calls" not in self.messages[-1]:
                self.messages[-1] = assistant_msg
            else:
                self.messages.append(assistant_msg)

            for tc in result.tool_calls:
                args = tc.parsed_args()
                print(f"  [工具] {tc.name}({args})")
                tool_result = self.skills.dispatch(tc.name, args)
                self._apply_state_change(tc.name, args, tool_result)
                print(f"  [结果] {tool_result[:200]}")
                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "name": tc.name,
                        "content": tool_result,
                    }
                )
            # 继续下一轮，让 LLM 基于工具结果继续
        else:
            print("[GM] (工具调用轮次已达上限，请继续输入下一条指令。)")

        self._trim_history()

    def _apply_state_change(self, tool_name: str, args: dict[str, Any], tool_result: str) -> None:
        if tool_name == "select_target" and tool_result.startswith("已选择"):
            self.current_state = "TRAIN"
        elif tool_name == "change_state":
            new_state = str(args.get("new_state", "")).upper()
            if new_state in ("TITLE", "SHOP", "TRAIN"):
                self.current_state = new_state
        elif tool_name == "advance_time":
            self.current_state = "SHOP"

    def _trim_history(self) -> None:
        if len(self.messages) <= MAX_HISTORY_MESSAGES + 1:
            return
        system = self.messages[0]
        rest = self.messages[1:]
        self.messages = [system] + rest[-MAX_HISTORY_MESSAGES:]
