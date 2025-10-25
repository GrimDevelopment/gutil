from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Dict, List


class LanceDBStoreError(RuntimeError):
    pass


@dataclass
class MemoryEntry:
    id: str
    ts: float
    prompt: str
    response: str
    tags: List[str]
    tokens: int
    embedding: List[float]


class LanceDBStore:
    def __init__(self, uri: str, table_name: str = "interactions") -> None:
        try:
            import lancedb
        except Exception as e:  # noqa: BLE001
            raise LanceDBStoreError(
                "lancedb is required. Install with: pip install lancedb"
            ) from e
        self.db = lancedb.connect(uri)
        self.table_name = table_name
        self._ensure_table()

    def _ensure_table(self) -> None:
        data = [
            {
                "id": "_schema_example_",
                "ts": time.time(),
                "prompt": "",
                "response": "",
                "tags": [],
                "tokens": 0,
                "embedding": [0.0],
            }
        ]
        if self.table_name not in [t.name for t in self.db.tables()]:
            self.db.create_table(self.table_name, data=data, exist_ok=True)
            # remove the example row
            self.db.open_table(self.table_name).delete("id == '_schema_example_'")

    def add(self, entry: MemoryEntry) -> None:
        tbl = self.db.open_table(self.table_name)
        tbl.add(
            [
                {
                    "id": entry.id,
                    "ts": entry.ts,
                    "prompt": entry.prompt,
                    "response": entry.response,
                    "tags": entry.tags,
                    "tokens": entry.tokens,
                    "embedding": entry.embedding,
                }
            ]
        )

    def search(self, vector: List[float], k: int = 5) -> List[Dict[str, Any]]:
        tbl = self.db.open_table(self.table_name)
        try:
            results = tbl.search(vector).limit(k).to_list()
        except Exception:
            # Some older versions use different APIs; fallback to Arrow
            results = tbl.search(vector).limit(k).to_arrow().to_pylist()
        return results

