from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional


class EmbeddingError(RuntimeError):
    pass


@dataclass
class EmbeddingConfig:
    provider: str = "fastembed"  # fastembed | openai
    model: Optional[str] = None   # optional override


class Embeddings:
    def __init__(self, cfg: EmbeddingConfig):
        self.cfg = cfg
        self._impl = self._init_impl(cfg)

    def _init_impl(self, cfg: EmbeddingConfig):
        if cfg.provider == "fastembed":
            try:
                from fastembed import TextEmbedding
            except Exception as e:  # noqa: BLE001
                raise EmbeddingError(
                    "fastembed is not installed. Install with: pip install fastembed"
                ) from e
            model = cfg.model or "BAAI/bge-small-en-v1.5"
            return TextEmbedding(model)
        elif cfg.provider == "openai":
            try:
                from openai import OpenAI
            except Exception as e:  # noqa: BLE001
                raise EmbeddingError(
                    "openai is not installed. Install with: pip install openai"
                ) from e
            model = cfg.model or "text-embedding-3-small"
            client = OpenAI()

            class _OpenAIEmb:
                def __init__(self, m, c):
                    self.model = m
                    self.client = c

                def embed(self, texts: List[str]) -> List[List[float]]:
                    resp = self.client.embeddings.create(model=self.model, input=texts)
                    return [d.embedding for d in resp.data]

            return _OpenAIEmb(model, client)
        else:
            raise EmbeddingError(f"Unknown embeddings provider: {cfg.provider}")

    def encode(self, texts: Iterable[str]) -> List[List[float]]:
        texts = list(texts)
        if not texts:
            return []
        # fastembed TextEmbedding returns a generator of vectors
        impl = self._impl
        if hasattr(impl, "embed"):
            return impl.embed(texts)  # type: ignore[no-any-return]
        # fastembed API
        vecs = impl.embed(texts)  # type: ignore[attr-defined]
        return [list(v) for v in vecs]

