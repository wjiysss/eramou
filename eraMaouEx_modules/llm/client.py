"""LLM 客户端 - OpenAI 兼容 chat/completions 接口

仅使用标准库，不引入外部依赖。
"""
from __future__ import annotations
import json
import urllib.request
import urllib.error
from typing import Any, Optional

from .config import LLMConfig


class LLMError(Exception):
    pass


class ToolCall:
    __slots__ = ("id", "name", "arguments")

    def __init__(self, call_id: str, name: str, arguments: str):
        self.id = call_id
        self.name = name
        self.arguments = arguments

    def parsed_args(self) -> dict[str, Any]:
        if not self.arguments:
            return {}
        try:
            parsed = json.loads(self.arguments)
            return parsed if isinstance(parsed, dict) else {"value": parsed}
        except Exception:
            return {"_raw": self.arguments}


class ChatResult:
    __slots__ = ("content", "tool_calls", "raw")

    def __init__(self, content: str, tool_calls: list[ToolCall], raw: dict[str, Any]):
        self.content = content
        self.tool_calls = tool_calls
        self.raw = raw


class LLMClient:
    def __init__(self, config: LLMConfig, timeout: int = 60):
        self.config = config
        self.timeout = timeout

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: Optional[list[dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> ChatResult:
        payload: dict[str, Any] = {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        payload["enable_thinking"] = False
        payload["thinking_budget"] = 0

        body = json.dumps(payload).encode("utf-8")
        last_error: Optional[Exception] = None

        for attempt in range(2):
            try:
                return self._do_request(body)
            except urllib.error.HTTPError as e:
                last_error = e
                detail = ""
                try:
                    detail = e.read().decode("utf-8", errors="replace")[:500]
                except Exception:
                    pass
                if attempt == 0 and e.code in (429, 500, 502, 503, 504):
                    continue
                raise LLMError(f"HTTP {e.code}: {detail}") from e
            except urllib.error.URLError as e:
                last_error = e
                if attempt == 0:
                    continue
                raise LLMError(f"网络错误: {e.reason}") from e
            except Exception as e:
                last_error = e
                if attempt == 0:
                    continue
                raise LLMError(f"请求失败: {e}") from e

        raise LLMError(f"请求重试后仍失败: {last_error}")

    def chat_stream(
        self,
        messages: list[dict[str, Any]],
        tools: Optional[list[dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ):
        """流式生成器：以 stream:true 调用接口，解析 SSE 逐 chunk 产出。

        yield 的 dict 类型：
        - {"type": "content_delta", "content": 增量文本}
        - {"type": "tool_calls_done", "tool_calls": [ToolCall, ...]}  # 流结束且有工具调用时
        - {"type": "done", "content": 完整content, "tool_calls": [ToolCall,...], "raw": {}}
        """
        payload: dict[str, Any] = {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        payload["enable_thinking"] = False
        payload["thinking_budget"] = 0

        body = json.dumps(payload).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Origin": "https://opencode.ai",
            "Referer": "https://opencode.ai/",
        }

        req = urllib.request.Request(
            self.config.base_url, data=body, headers=headers, method="POST"
        )

        full_content: list[str] = []
        tool_calls_acc: list[dict[str, str]] = []

        try:
            resp = urllib.request.urlopen(req, timeout=self.timeout)
        except urllib.error.HTTPError as e:
            detail = ""
            try:
                detail = e.read().decode("utf-8", errors="replace")[:500]
            except Exception:
                pass
            raise LLMError(f"HTTP {e.code}: {detail}") from e
        except urllib.error.URLError as e:
            raise LLMError(f"网络错误: {e.reason}") from e
        except Exception as e:
            raise LLMError(f"请求失败: {e}") from e

        try:
            buffer = ""
            for raw_line in resp:
                line = raw_line.decode("utf-8", errors="replace").rstrip("\r\n")

                if line == "":
                    if buffer:
                        evt = self._parse_sse_chunk(
                            buffer, full_content, tool_calls_acc
                        )
                        if evt:
                            yield evt
                        buffer = ""
                    continue

                if line.startswith("data:"):
                    data_str = line[5:].lstrip()
                    if data_str.strip() == "[DONE]":
                        break
                    buffer = (buffer + "\n" + data_str) if buffer else data_str
        finally:
            try:
                resp.close()
            except Exception:
                pass

        if buffer:
            evt = self._parse_sse_chunk(buffer, full_content, tool_calls_acc)
            if evt:
                yield evt

        final_tool_calls: list[ToolCall] = []
        if tool_calls_acc:
            for tc in tool_calls_acc:
                if tc.get("name") or tc.get("id") or tc.get("arguments"):
                    final_tool_calls.append(
                        ToolCall(
                            call_id=tc.get("id", ""),
                            name=tc.get("name", ""),
                            arguments=tc.get("arguments", "") or "",
                        )
                    )
            if final_tool_calls:
                yield {
                    "type": "tool_calls_done",
                    "tool_calls": final_tool_calls,
                }

        yield {
            "type": "done",
            "content": "".join(full_content),
            "tool_calls": final_tool_calls,
            "raw": {},
        }

    @staticmethod
    def _parse_sse_chunk(
        buffer: str,
        full_content: list[str],
        tool_calls_acc: list[dict[str, str]],
    ) -> Optional[dict[str, Any]]:
        try:
            data = json.loads(buffer)
        except Exception:
            return None
        choices = data.get("choices") or []
        if not choices:
            return None
        delta = choices[0].get("delta", {}) or {}

        piece = delta.get("content")
        if piece:
            full_content.append(piece)
            return {"type": "content_delta", "content": piece}

        tcs_delta = delta.get("tool_calls")
        if tcs_delta:
            for tc in tcs_delta:
                idx = tc.get("index", 0)
                while len(tool_calls_acc) <= idx:
                    tool_calls_acc.append({"id": "", "name": "", "arguments": ""})
                func = tc.get("function", {}) or {}
                if tc.get("id"):
                    tool_calls_acc[idx]["id"] = tc["id"]
                if func.get("name"):
                    tool_calls_acc[idx]["name"] = func["name"]
                if func.get("arguments"):
                    tool_calls_acc[idx]["arguments"] += func["arguments"]
        return None

    def _do_request(self, body: bytes) -> ChatResult:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Origin": "https://opencode.ai",
            "Referer": "https://opencode.ai/",
        }
        req = urllib.request.Request(
            self.config.base_url, data=body, headers=headers, method="POST"
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            raw_text = resp.read().decode("utf-8", errors="replace")

        try:
            data = json.loads(raw_text)
        except Exception as e:
            raise LLMError(f"解析响应失败: {e}\n原始响应前500字: {raw_text[:500]}") from e

        choices = data.get("choices") or []
        if not choices:
            raise LLMError(f"响应无 choices: {raw_text[:300]}")

        message = choices[0].get("message", {})
        content = message.get("content") or ""
        tool_calls_raw = message.get("tool_calls") or []

        tool_calls: list[ToolCall] = []
        for tc in tool_calls_raw:
            func = tc.get("function", {})
            tool_calls.append(
                ToolCall(
                    call_id=tc.get("id", ""),
                    name=func.get("name", ""),
                    arguments=func.get("arguments", "") or "",
                )
            )

        return ChatResult(content=content, tool_calls=tool_calls, raw=data)
