from pydantic import BaseModel
from typing import Optional

class CodexRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7

class CodexResponse(BaseModel):
    id: str
    object: str
    created: int
    choices: list[dict]
    usage: dict

class CodexError(BaseModel):
    error: str
    message: str