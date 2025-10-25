from __future__ import annotations

from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7


class GenerateResponse(BaseModel):
    text: str
    tokens: int | None = None
    meta: Dict[str, Any] | None = None

