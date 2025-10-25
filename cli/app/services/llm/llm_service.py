from __future__ import annotations

from typing import Any, Dict


class LLMService:
    """Placeholder for CLI LLM generation service.

    Wire to Codex CLI or a backend later.
    """

    async def generate(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        raise NotImplementedError

