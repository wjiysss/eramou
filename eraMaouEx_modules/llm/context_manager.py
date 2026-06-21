"""上下文管理：token 预算估算、tool 配对保护裁剪、摘要压缩。

替代旧的硬编码「>22 条就裁剪」逻辑。保证：
1. tool_call/tool_result 配对不被拆散（避免 LLM API 400 错误）
2. 超预算时优先尝试摘要压缩（保留剧情），失败则降级为纯裁剪
3. embedding/LLM 失败时优雅降级
"""
from __future__ import annotations
from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .client import LLMClient


class ContextManager:
    def __init__(
        self,
        max_tokens: int = 8000,
        compress_threshold: float = 0.85,
        summary_keep_recent: int = 6,
    ):
        self.max_tokens = max_tokens  # 预算上限（token 近似）
        self.compress_threshold = compress_threshold  # 达到预算多少比例触发压缩
        self.summary_keep_recent = summary_keep_recent  # 压缩时保留最近多少条不压缩

    def estimate_tokens(self, messages: list[dict[str, Any]]) -> int:
        """字符加权近似：中文 1 字 ≈ 1 token，英文约 4 字符 ≈ 1 token，tool_calls 结构额外加权。
        简单实现：对每条消息，按 content 长度 + tool_calls 结构长度估算，求和。
        """
        total = 0
        for m in messages:
            content = m.get("content") or ""
            if isinstance(content, str):
                total += len(content)
            elif isinstance(content, list):
                for part in content:
                    if isinstance(part, dict):
                        total += len(str(part.get("text", "")))
            # tool_calls 结构加权
            tcs = m.get("tool_calls")
            if isinstance(tcs, list):
                for tc in tcs:
                    func = tc.get("function", {}) if isinstance(tc, dict) else {}
                    total += len(str(func.get("arguments", ""))) + 20
            # role 标签开销
            total += 4
        return total

    def manage(
        self,
        messages: list[dict[str, Any]],
        llm_client: "Optional[LLMClient]" = None,
    ) -> list[dict[str, Any]]:
        """主入口：根据预算管理 messages，返回新列表（不原地修改）。

        流程：
        1. 若 estimate_tokens(messages) <= max_tokens * compress_threshold，原样返回。
        2. 否则先尝试压缩（若有 llm_client）：把最早的一批消息（保留最近 summary_keep_recent 条 +
           所有 system 消息 + 当前 tool 配对组）打包成摘要，用 LLM 生成"剧情摘要"system 消息替换。
        3. 压缩失败/无 LLM：降级为 trim_with_pairing 纯裁剪。
        """
        budget_soft = int(self.max_tokens * self.compress_threshold)
        if self.estimate_tokens(messages) <= budget_soft:
            return list(messages)
        # 尝试压缩
        if llm_client is not None:
            try:
                compressed = self._compress(messages, llm_client)
                if compressed is not None and self.estimate_tokens(compressed) <= budget_soft:
                    return compressed
            except Exception as e:
                print(f"[ContextManager] 压缩失败，降级裁剪: {e}")
        # 降级裁剪
        return self.trim_with_pairing(messages, budget_soft)

    def trim_with_pairing(self, messages: list[dict[str, Any]], budget_tokens: int) -> list[dict[str, Any]]:
        """从尾部保留消息，遇 tool 消息连带其 assistant(tool_calls) 父消息，直到预算用尽。

        算法：
        1. 总是保留开头的所有 system 消息（通常是 1 条）。
        2. 从尾部向前扫描，累积保留消息。
        3. 遇到 role=tool 的消息时，必须向前回溯找到对应的 assistant(tool_calls) 父消息（通过 tool_call_id 匹配），
           把整组（assistant + 所有相关 tool 结果）一起保留。
        4. 估算累积 tokens，超过 budget 就停止（但已纳入的配对组必须完整保留）。
        """
        if not messages:
            return []
        # 1. 保留开头 system 消息
        head_systems: list[dict[str, Any]] = []
        i = 0
        while i < len(messages) and messages[i].get("role") == "system":
            head_systems.append(messages[i])
            i += 1
        rest = messages[i:]
        if not rest:
            return list(head_systems)

        # 2. 从尾部向前，按配对组累积
        # 先把 rest 切分为「配对组」单元：每个 assistant(tool_calls) + 紧随其后的所有 tool 消息为一组；
        # 其它消息（user/普通 assistant）各自为一组。
        groups = self._split_into_groups(rest)
        # 从尾部累积
        kept_groups: list[list[dict[str, Any]]] = []
        used_tokens = self.estimate_tokens(head_systems)
        for grp in reversed(groups):
            grp_tokens = self.estimate_tokens(grp)
            if used_tokens + grp_tokens > budget_tokens and kept_groups:
                # 预算用尽（但若 kept_groups 为空，至少保留一组避免空消息）
                break
            kept_groups.append(grp)
            used_tokens += grp_tokens
        kept_groups.reverse()
        out = list(head_systems)
        for grp in kept_groups:
            out.extend(grp)
        return out

    def _split_into_groups(self, messages: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
        """把消息序列切成配对组。assistant(tool_calls) + 紧随其后的所有 tool 消息为一组。"""
        groups: list[list[dict[str, Any]]] = []
        i = 0
        n = len(messages)
        while i < n:
            m = messages[i]
            if m.get("role") == "assistant" and m.get("tool_calls"):
                grp = [m]
                i += 1
                # 收集紧随的 tool 消息
                while i < n and messages[i].get("role") == "tool":
                    grp.append(messages[i])
                    i += 1
                groups.append(grp)
            else:
                groups.append([m])
                i += 1
        return groups

    def _compress(
        self,
        messages: list[dict[str, Any]],
        llm_client: "LLMClient",
    ) -> Optional[list[dict[str, Any]]]:
        """摘要压缩：把较早的消息打包，调用 LLM 生成摘要，替换为单条 system 消息。"""
        # 仅保留第一条 system 消息（live sys_prompt）；历史摘要 system 会被折叠进新摘要
        head_systems: list[dict[str, Any]] = []
        if messages and messages[0].get("role") == "system":
            head_systems.append(messages[0])
            rest = messages[1:]
        else:
            rest = list(messages)
        if len(rest) <= self.summary_keep_recent:
            return None  # 没东西可压缩
        groups = self._split_into_groups(rest)
        # 保留末尾若干组（覆盖至少 summary_keep_recent 条消息）
        kept_tail: list[list[dict[str, Any]]] = []
        kept_count = 0
        cut = len(groups)
        for j in range(len(groups) - 1, -1, -1):
            if kept_count >= self.summary_keep_recent:
                cut = j + 1
                break
            kept_tail.insert(0, groups[j])
            kept_count += len(groups[j])
        else:
            cut = 0
        to_compress = []
        for j in range(cut):
            to_compress.extend(groups[j])
        if not to_compress:
            return None
        # 打包成纯文本喂给 LLM
        transcript = self._render_transcript(to_compress)
        summary_prompt = (
            "你是剧情摘要器。请把下面的游戏对话/动作历史压缩为一段 200~400 字的中文剧情摘要，"
            "保留：关键事件、角色状态变化、玩家意图、数值变化。去掉寒暄和冗余描写。\n\n"
            "=== 历史 ===\n" + transcript
        )
        try:
            result = llm_client.chat(
                [{"role": "user", "content": summary_prompt}],
                tools=None,
                temperature=0.3,
                max_tokens=600,
            )
            summary_text = (result.content or "").strip()
            if not summary_text:
                return None
        except Exception as e:
            print(f"[ContextManager] 摘要 LLM 调用失败: {e}")
            return None
        # 构造新消息：原 system + 摘要 system + 保留的尾部
        summary_msg = {
            "role": "system",
            "content": f"=== 剧情摘要（之前发生的事）===\n{summary_text}",
        }
        out = list(head_systems) + [summary_msg]
        for grp in kept_tail:
            out.extend(grp)
        return out

    def _render_transcript(self, messages: list[dict[str, Any]]) -> str:
        """把消息序列渲染为可读纯文本（喂给摘要 LLM）。"""
        lines: list[str] = []
        for m in messages:
            role = m.get("role", "?")
            if role == "system":
                continue  # 摘要不重复 system
            content = m.get("content") or ""
            if role == "tool":
                name = m.get("name", "tool")
                lines.append(f"[工具结果:{name}] {content[:200]}")
            elif role == "assistant":
                tcs = m.get("tool_calls")
                if tcs:
                    names = []
                    for tc in tcs:
                        func = tc.get("function", {}) if isinstance(tc, dict) else {}
                        names.append(func.get("name", "?"))
                    lines.append(f"[GM 调用工具: {', '.join(names)}] {content[:150]}")
                else:
                    lines.append(f"[GM] {content[:300]}")
            elif role == "user":
                lines.append(f"[玩家] {content[:300]}")
        return "\n".join(lines)
