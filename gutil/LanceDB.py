from __future__ import annotations

import json
from typing import Any, Iterable, List, Mapping, Optional


class LanceDBNotInstalled(RuntimeError):
    pass


def _ensure_lancedb():
    try:
        import lancedb  # noqa: F401
    except Exception as e:  # noqa: BLE001
        raise LanceDBNotInstalled(
            "lancedb is required for this feature. Install with: pip install lancedb"
        ) from e


class LanceDBClient:
    """Minimal LanceDB helper to keep integration lightweight.

    Library methods raise on error and avoid printing. The CLI layer handles I/O.
    """

    def __init__(self, uri: str):
        if not uri:
            raise ValueError("A LanceDB URI/path is required")
        _ensure_lancedb()
        import lancedb  # type: ignore

        self._db = lancedb.connect(uri)

    def list_tables(self) -> List[str]:
        return [t.name for t in self._db.tables()]

    def create_table(
        self, name: str, rows: Iterable[Mapping[str, Any]], exist_ok: bool = False
    ) -> None:
        if not name:
            raise ValueError("Table name must be non-empty")
        data = list(rows)
        if not data:
            raise ValueError("At least one row is required to create a table")
        self._db.create_table(name, data=data, exist_ok=exist_ok)

    def insert(self, name: str, rows: Iterable[Mapping[str, Any]]) -> int:
        tbl = self._db.open_table(name)
        data = list(rows)
        if not data:
            return 0
        tbl.add(data)
        return len(data)

    def query(self, name: str, limit: Optional[int] = None) -> List[Mapping[str, Any]]:
        tbl = self._db.open_table(name)
        arrow = tbl.to_arrow(limit=limit)
        return arrow.to_pylist()

    @staticmethod
    def load_json_file(path: str) -> List[Mapping[str, Any]]:
        with open(path, "r", encoding="utf-8") as f:
            content = json.load(f)
        if isinstance(content, dict):
            return [content]
        if isinstance(content, list):
            return content  # type: ignore[return-value]
        raise ValueError("JSON must be an object or an array of objects")

