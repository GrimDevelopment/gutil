from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from typing import List, Sequence

from ..embeddings import Embeddings, EmbeddingConfig
from ..lancedb_store import LanceDBStore, MemoryEntry


@dataclass
class RetrievalConfig:
    top_k: int = 5


class ContextManager:
    def __init__(self, store: LanceDBStore, embeddings: Embeddings, rcfg: RetrievalConfig):
        self.store = store
        self.embeddings = embeddings
        self.rcfg = rcfg

    def retrieve(self, prompt: str) -> List[dict]:
        vec = self.embeddings.encode([prompt])[0]
        results = self.store.search(vec, k=self.rcfg.top_k)
        return results

    def remember(self, prompt: str, response: str, tags: Sequence[str] = ()) -> MemoryEntry:
        vec = self.embeddings.encode([prompt + "\n\n" + response])[0]
        entry = MemoryEntry(
            id=str(uuid.uuid4()),
            ts=time.time(),
            prompt=prompt,
            response=response,
            tags=list(tags),
            tokens=len(prompt.split()) + len(response.split()),
            embedding=list(vec),
        )
        self.store.add(entry)
        return entry

