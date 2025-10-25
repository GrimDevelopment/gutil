from typing import Any, Dict
import httpx

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Any:
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, json=data)
            response.raise_for_status()
            return response.json()

    async def get(self, endpoint: str) -> Any:
        return await self.request("GET", endpoint)

    async def post(self, endpoint: str, data: Dict[str, Any]) -> Any:
        return await self.request("POST", endpoint, data)

    async def put(self, endpoint: str, data: Dict[str, Any]) -> Any:
        return await self.request("PUT", endpoint, data)

    async def delete(self, endpoint: str) -> Any:
        return await self.request("DELETE", endpoint)