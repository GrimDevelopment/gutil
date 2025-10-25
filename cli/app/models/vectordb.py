from __future__ import annotations

from typing import List, Dict, Any
from pydantic import BaseModel


class VectorRecord(BaseModel):
    id: str
    vector: List[float]
    payload: Dict[str, Any] = {}

