from typing import List
from pydantic import BaseModel
import requests

class EmbeddingRequest(BaseModel):
    text: str

class EmbeddingResponse(BaseModel):
    embeddings: List[float]

class EmbeddingService:
    def __init__(self, api_url: str):
        self.api_url = api_url

    async def get_embeddings(self, request: EmbeddingRequest) -> EmbeddingResponse:
        try:
            response = requests.post(f"{self.api_url}/embeddings", json=request.dict())
            response.raise_for_status()
            return EmbeddingResponse(**response.json())
        except requests.HTTPError as e:
            raise Exception(f"HTTP error occurred: {e}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")