from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

from ..core.state import load_app_config, save_app_config


@dataclass
class AppSettings:
    api_url: str
    token: Optional[str] = None
    generate_endpoint: str = "/api/v1/codex/generate"
    health_endpoint: str = "/api/v1/health/health"

    @staticmethod
    def from_config() -> "AppSettings":
        cfg = load_app_config()
        return AppSettings(
            api_url=cfg.get("api_url", "http://localhost:8000"),
            token=cfg.get("token"),
            generate_endpoint=cfg.get("generate_endpoint", "/api/v1/codex/generate"),
            health_endpoint=cfg.get("health_endpoint", "/api/v1/health/health"),
        )

    def persist(self) -> None:
        cfg = load_app_config()
        cfg.update(
            {
                "api_url": self.api_url,
                "token": self.token,
                "generate_endpoint": self.generate_endpoint,
                "health_endpoint": self.health_endpoint,
            }
        )
        save_app_config(cfg)


class AppClient:
    def __init__(self, settings: Optional[AppSettings] = None):
        self.settings = settings or AppSettings.from_config()

    def _headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {"Content-Type": "application/json"}
        if self.settings.token:
            headers["Authorization"] = f"Bearer {self.settings.token}"
        return headers

    def login(self, email: str, password: str) -> Dict[str, Any]:
        url = f"{self.settings.api_url}/api/v1/auth/login"
        resp = requests.post(url, json={"email": email, "password": password}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        token = data.get("access_token")
        if token:
            self.settings.token = token
            self.settings.persist()
        return data

    def logout(self) -> Dict[str, Any]:
        url = f"{self.settings.api_url}/api/v1/auth/logout"
        resp = requests.post(url, headers=self._headers(), timeout=30)
        resp.raise_for_status()
        # Clear local token
        self.settings.token = None
        self.settings.persist()
        return resp.json()

    def register(self, email: str, password: str) -> Dict[str, Any]:
        url = f"{self.settings.api_url}/api/v1/auth/register"
        resp = requests.post(url, json={"email": email, "password": password}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def generate(self, prompt: str, max_tokens: int = 100) -> Dict[str, Any]:
        url = f"{self.settings.api_url}{self.settings.generate_endpoint}"
        payload = {"prompt": prompt, "max_tokens": max_tokens}
        resp = requests.post(url, headers=self._headers(), json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()

    def health(self) -> bool:
        url = f"{self.settings.api_url}{self.settings.health_endpoint}"
        try:
            r = requests.get(url, timeout=5)
            return r.status_code == 200
        except requests.RequestException:
            return False

