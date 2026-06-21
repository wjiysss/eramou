"""Embedding 客户端：调用 OpenAI 兼容的 /v1/embeddings 接口。

用于 RAG 检索的文本向量化。失败时抛 EmbeddingError，由上层（rag/web）捕获降级。
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Optional

from .config import EmbeddingConfig


class EmbeddingError(RuntimeError):
    pass


class EmbeddingClient:
    def __init__(self, config: EmbeddingConfig, timeout: int = 30):
        self.config = config
        self.timeout = timeout

    def embed(self, text: str) -> list[float]:
        vecs = self.embed_batch([text])
        return vecs[0] if vecs else []

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        payload: dict[str, Any] = {
            "model": self.config.model,
            "input": texts,
        }
        body = json.dumps(payload).encode("utf-8")
        last_error: Optional[Exception] = None
        for attempt in range(2):
            try:
                return self._do_request(body, expected=len(texts))
            except urllib.error.HTTPError as e:
                last_error = e
                detail = ""
                try:
                    detail = e.read().decode("utf-8", errors="replace")[:500]
                except Exception:
                    pass
                if attempt == 0 and e.code in (429, 500, 502, 503, 504):
                    continue
                raise EmbeddingError(f"HTTP {e.code}: {detail}") from e
            except urllib.error.URLError as e:
                last_error = e
                if attempt == 0:
                    continue
                raise EmbeddingError(f"网络错误: {e.reason}") from e
            except EmbeddingError:
                raise
            except Exception as e:
                last_error = e
                if attempt == 0:
                    continue
                raise EmbeddingError(f"请求失败: {e}") from e
        raise EmbeddingError(f"请求重试后仍失败: {last_error}")

    def _do_request(self, body: bytes, expected: int) -> list[list[float]]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        req = urllib.request.Request(
            self.config.base_url, data=body, headers=headers, method="POST"
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            raw_text = resp.read().decode("utf-8", errors="replace")
        try:
            data = json.loads(raw_text)
        except Exception as e:
            raise EmbeddingError(f"解析响应失败: {e}\n原始响应前500字: {raw_text[:500]}") from e

        # OpenAI 兼容格式：{"data": [{"embedding": [...]}, ...]}
        items = data.get("data") or []
        result: list[list[float]] = []
        for item in items:
            vec = item.get("embedding")
            if isinstance(vec, list):
                result.append([float(x) for x in vec])
        if len(result) < expected:
            raise EmbeddingError(
                f"返回向量数 {len(result)} 少于请求 {expected}；响应前200字: {raw_text[:200]}"
            )
        # 按 index 排序确保顺序
        order = sorted(
            range(len(items)),
            key=lambda i: items[i].get("index", i),
        )
        return [result[i] for i in range(len(result))][: len(items)] or result
