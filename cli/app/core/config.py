from __future__ import annotations

from pydantic import BaseSettings


class CLISettings(BaseSettings):
    api_url: str = "http://localhost:8000"
    timeout: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

