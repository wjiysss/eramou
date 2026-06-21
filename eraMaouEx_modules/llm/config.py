"""LLM 配置加载

从环境变量或本地 .env 文件读取 api_key / base_url / model。
密钥不入库：.env 与 llm_config.local.json 已加入 .gitignore。
"""
from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


DEFAULT_BASE_URL = "https://opencode.ai/zen/go/v1/chat/completions"
DEFAULT_MODEL = "deepseek-v4-flash"

_ENV_KEY_API = "ERAMOU_LLM_API_KEY"
_ENV_KEY_BASE = "ERAMOU_LLM_BASE_URL"
_ENV_KEY_MODEL = "ERAMOU_LLM_MODEL"

# Embedding（RAG 检索用）配置键
_ENV_EMB_API = "ERAMOU_EMB_API_KEY"
_ENV_EMB_BASE = "ERAMOU_EMB_BASE_URL"
_ENV_EMB_MODEL = "ERAMOU_EMB_MODEL"
DEFAULT_EMB_BASE = "https://router.tumuer.me/v1/embeddings"
DEFAULT_EMB_MODEL = "Qwen/Qwen3-Embedding-4B"


@dataclass
class LLMConfig:
    api_key: str
    base_url: str
    model: str


@dataclass
class EmbeddingConfig:
    api_key: str
    base_url: str
    model: str


def _parse_env_file(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not path.exists():
        return result
    try:
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            result[key.strip()] = value.strip().strip('"').strip("'")
    except Exception:
        pass
    return result


def _candidate_env_paths() -> list[Path]:
    here = Path(__file__).resolve()
    return [
        here.parent.parent.parent / ".env",
        Path.cwd() / ".env",
    ]


def load_config(silent: bool = False) -> Optional[LLMConfig]:
    api_key = os.environ.get(_ENV_KEY_API)
    base_url = os.environ.get(_ENV_KEY_BASE) or DEFAULT_BASE_URL
    model = os.environ.get(_ENV_KEY_MODEL) or DEFAULT_MODEL

    if not api_key:
        for env_path in _candidate_env_paths():
            data = _parse_env_file(env_path)
            if not api_key and data.get(_ENV_KEY_API):
                api_key = data[_ENV_KEY_API]
            if not base_url or base_url == DEFAULT_BASE_URL:
                base_url = data.get(_ENV_KEY_BASE, base_url)
            if not model or model == DEFAULT_MODEL:
                model = data.get(_ENV_KEY_MODEL, model)
            if api_key:
                break

    if not api_key:
        if not silent:
            print("[LLM] 未找到 api_key。请设置环境变量 ERAMOU_LLM_API_KEY 或在项目根目录创建 .env 文件。")
            print(f"[LLM] 可参考 .env.example。所需变量：{_ENV_KEY_API} / {_ENV_KEY_BASE} / {_ENV_KEY_MODEL}")
        return None

    return LLMConfig(api_key=api_key, base_url=base_url, model=model)


def load_embedding_config(silent: bool = False) -> Optional[EmbeddingConfig]:
    """加载 embedding 配置。缺失时返回 None（RAG 将优雅降级为不注入）。"""
    api_key = os.environ.get(_ENV_EMB_API)
    base_url = os.environ.get(_ENV_EMB_BASE) or DEFAULT_EMB_BASE
    model = os.environ.get(_ENV_EMB_MODEL) or DEFAULT_EMB_MODEL

    if not api_key:
        for env_path in _candidate_env_paths():
            data = _parse_env_file(env_path)
            if not api_key and data.get(_ENV_EMB_API):
                api_key = data[_ENV_EMB_API]
            if not base_url or base_url == DEFAULT_EMB_BASE:
                base_url = data.get(_ENV_EMB_BASE, base_url)
            if not model or model == DEFAULT_EMB_MODEL:
                model = data.get(_ENV_EMB_MODEL, model)
            if api_key:
                break

    if not api_key:
        if not silent:
            print("[LLM] 未找到 embedding api_key，RAG 检索将禁用。")
            print(f"[LLM] 所需变量：{_ENV_EMB_API} / {_ENV_EMB_BASE} / {_ENV_EMB_MODEL}")
        return None

    return EmbeddingConfig(api_key=api_key, base_url=base_url, model=model)
