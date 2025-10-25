from __future__ import annotations

from typing import List


class EmbeddingService:
    """Placeholder for CLI embedding pipeline.

    Implement with fastembed or OpenAI later.
    """

    def embed(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError

