"""RAG 检索：游戏知识的向量索引与检索。

三类知识：
- 静态：天赋说明（Talent.csv）+ ERB 机制文档（erb_knowledge.build_static_knowledge）
- 动态：游戏事件历史（运行时累积）

向量存储纯标准库（JSON 持久化 + 余弦相似度）。embedding 不可用时优雅降级。
"""
from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass, field, asdict
from typing import Any, Optional

from .embedding import EmbeddingClient, EmbeddingError


@dataclass
class KnowledgeEntry:
    text: str
    vector: list[float] = field(default_factory=list)
    source: str = ""            # "talent" / "erb" / "event"
    metadata: dict[str, Any] = field(default_factory=dict)


def _cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = 0.0
    na = 0.0
    nb = 0.0
    for x, y in zip(a, b):
        dot += x * y
        na += x * x
        nb += y * y
    if na <= 0.0 or nb <= 0.0:
        return 0.0
    return dot / (math.sqrt(na) * math.sqrt(nb))


def _tokenize_cjk(text: str) -> list[str]:
    """简易中文分词：CJK 字符做 bigram，非 CJK 按空白切词。用于关键词召回。"""
    import re
    tokens: list[str] = []
    # 提取连续 CJK 片段
    for seg in re.findall(r"[\u4e00-\u9fff]+", text):
        if len(seg) >= 2:
            for i in range(len(seg) - 1):
                tokens.append(seg[i:i + 2])
        tokens.append(seg)
    # 非 CJK 词
    for seg in re.findall(r"[A-Za-z0-9]+", text):
        if len(seg) >= 2:
            tokens.append(seg.lower())
    return tokens


class KnowledgeIndex:
    """单一来源的知识索引（如 talent / erb / event），可持久化到 JSON。"""

    def __init__(self, path: str):
        self.path = path
        self.entries: list[KnowledgeEntry] = []
        self._dirty = False

    def load(self) -> bool:
        if not os.path.exists(self.path):
            return False
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.entries = [
                KnowledgeEntry(
                    text=e.get("text", ""),
                    vector=e.get("vector", []) or [],
                    source=e.get("source", ""),
                    metadata=e.get("metadata", {}) or {},
                )
                for e in data.get("entries", [])
            ]
            return True
        except Exception as e:
            print(f"[RAG] 加载索引失败 {self.path}: {e}")
            return False

    def save(self) -> None:
        if not self._dirty and os.path.exists(self.path):
            return
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            payload = {"entries": [asdict(e) for e in self.entries]}
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False)
            self._dirty = False
        except Exception as e:
            print(f"[RAG] 保存索引失败 {self.path}: {e}")

    def add(self, entry: KnowledgeEntry) -> None:
        if entry.vector:
            self.entries.append(entry)
            self._dirty = True

    def add_many(self, entries: list[KnowledgeEntry]) -> None:
        for e in entries:
            if e.vector:
                self.entries.append(e)
                self._dirty = True

    def search(self, query_vec: list[float], top_k: int = 4) -> list[tuple[KnowledgeEntry, float]]:
        if not query_vec or not self.entries:
            return []
        scored = [(_cosine(query_vec, e.vector), e) for e in self.entries]
        scored.sort(key=lambda t: t[0], reverse=True)
        out: list[tuple[KnowledgeEntry, float]] = []
        for score, e in scored:
            if score <= 0.0:
                break
            out.append((e, score))
            if len(out) >= top_k:
                break
        return out


class RAGSystem:
    """RAG 总管：持有 embedding 客户端与三类索引，提供检索与事件记录。"""

    def __init__(
        self,
        embedder: Optional[EmbeddingClient],
        index_dir: str,
    ):
        self.embedder = embedder
        self.index_dir = index_dir
        os.makedirs(index_dir, exist_ok=True)
        self.static_index = KnowledgeIndex(os.path.join(index_dir, "static.json"))
        self.event_index = KnowledgeIndex(os.path.join(index_dir, "events.json"))
        self._embed_ok = embedder is not None

    @property
    def available(self) -> bool:
        return self._embed_ok and self.embedder is not None

    # ---- 静态知识构建 ----
    def build_static_if_needed(self, texts_and_sources: list[tuple[str, str, dict]]) -> None:
        """若静态索引为空，用给定文本构建。texts_and_sources: [(text, source, metadata), ...]"""
        if self.static_index.load() and self.static_index.entries:
            print(f"[RAG] 静态索引已缓存: {len(self.static_index.entries)} 条")
            return
        if not self.available:
            print("[RAG] embedding 不可用，跳过静态索引构建")
            return
        texts = [t for t, _, _ in texts_and_sources]
        if not texts:
            return
        try:
            # 分批 embedding（每批 16 条，避免请求过大）
            vectors: list[list[float]] = []
            for i in range(0, len(texts), 16):
                vectors.extend(self.embedder.embed_batch(texts[i:i + 16]))
        except EmbeddingError as e:
            print(f"[RAG] 静态索引 embedding 失败: {e}")
            self._embed_ok = False
            return
        entries = []
        for (text, source, meta), vec in zip(texts_and_sources, vectors):
            entries.append(KnowledgeEntry(text=text, vector=vec, source=source, metadata=meta))
        self.static_index.add_many(entries)
        self.static_index.save()
        print(f"[RAG] 静态索引构建完成: {len(entries)} 条 → {self.static_index.path}")

    # ---- 事件历史 ----
    def record_event(self, text: str, metadata: Optional[dict] = None) -> None:
        if not text.strip():
            return
        if not self.available:
            self.event_index.add(KnowledgeEntry(text=text.strip(), source="event", metadata=metadata or {}))
            self.event_index.save()
            return
        try:
            vec = self.embedder.embed(text)
        except EmbeddingError as e:
            print(f"[RAG] 事件 embedding 失败，仅存文本: {e}")
            vec = []
        self.event_index.add(KnowledgeEntry(text=text.strip(), vector=vec, source="event", metadata=metadata or {}))
        self.event_index.save()

    def load_events(self) -> None:
        self.event_index.load()

    # ---- 检索 ----
    def retrieve(self, query_text: str, top_k: int = 4) -> list[tuple[KnowledgeEntry, float]]:
        if not query_text.strip():
            return []
        # 关键词召回：对 query 中的中文 token，若 entry.text 命中则加分
        kw_tokens = [t for t in _tokenize_cjk(query_text) if len(t) >= 2]
        kw_results = self._keyword_recall(kw_tokens, top_k=top_k * 2)

        if not self.available:
            # 降级：仅关键词召回 + 最近事件
            recent = self.event_index.entries[-top_k:] if self.event_index.entries else []
            seen: set[str] = set()
            merged: list[tuple[KnowledgeEntry, float]] = []
            for e, s in kw_results:
                if e.text[:64] in seen:
                    continue
                seen.add(e.text[:64])
                merged.append((e, s))
            for e in recent:
                if e.text[:64] in seen:
                    continue
                seen.add(e.text[:64])
                merged.append((e, 0.0))
            return merged[:top_k]

        try:
            qv = self.embedder.embed(query_text)
        except EmbeddingError as e:
            print(f"[RAG] 检索 embedding 失败，降级关键词: {e}")
            return kw_results[:top_k]
        if not qv:
            return kw_results[:top_k]

        # 语义检索
        seen2: set[str] = set()
        scored: dict[str, tuple[KnowledgeEntry, float]] = {}
        for idx in (self.static_index, self.event_index):
            for e, score in idx.search(qv, top_k=top_k * 2):
                key = e.text[:64]
                if key in seen2:
                    continue
                seen2.add(key)
                # 混合评分：语义 0.7 + 关键词 0.3
                kw_bonus = 0.0
                if kw_tokens and any(tok in e.text for tok in kw_tokens):
                    kw_bonus = 0.3
                scored[key] = (e, score * 0.7 + kw_bonus)
        # 合入纯关键词召回（语义未覆盖的）
        for e, s in kw_results:
            key = e.text[:64]
            if key not in scored:
                scored[key] = (e, s * 0.3)

        merged = sorted(scored.values(), key=lambda t: t[1], reverse=True)
        return merged[:top_k]

    def _keyword_recall(self, tokens: list[str], top_k: int = 8) -> list[tuple[KnowledgeEntry, float]]:
        if not tokens:
            return []
        out: list[tuple[KnowledgeEntry, float]] = []
        for idx in (self.static_index, self.event_index):
            for e in idx.entries:
                hits = sum(1 for tok in tokens if tok in e.text)
                if hits > 0:
                    out.append((e, min(1.0, hits / max(1, len(tokens)))))
        out.sort(key=lambda t: t[1], reverse=True)
        return out[:top_k]

    def format_for_prompt(self, results: list[tuple[KnowledgeEntry, float]], max_chars: int = 800) -> str:
        if not results:
            return ""
        source_label = {"talent": "天赋说明", "erb": "ERB 机制", "event": "事件历史"}.get
        lines: list[str] = []
        total = 0
        for e, score in results:
            label = source_label(e.source, e.source)
            line = f"[{label}] {e.text}"
            if total + len(line) > max_chars:
                break
            lines.append(line)
            total += len(line)
        return "\n".join(lines)
