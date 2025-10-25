from __future__ import annotations


class QdrantService:
    """Placeholder for Qdrant client wrappers for CLI usage."""

    async def upsert(self, collection: str, vectors):
        raise NotImplementedError

    async def search(self, collection: str, vector, limit: int = 5):
        raise NotImplementedError

