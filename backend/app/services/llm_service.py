from typing import Any, Dict
import requests

class CodexService:
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url

    async def generate_code(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt,
            "max_tokens": kwargs.get("max_tokens", 150),
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 1.0),
            "n": kwargs.get("n", 1),
            "stop": kwargs.get("stop", None)
        }
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error generating code: {str(e)}") from e

    async def get_model_info(self) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        try:
            response = requests.get(f"{self.api_url}/models", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching model info: {str(e)}") from e