from typing import Any, Dict, List
from supabase import create_client, Client
from fastapi import HTTPException

class SupabaseDatabaseService:
    def __init__(self, table_name: str, response_model: Any):
        self.table_name = table_name
        self.response_model = response_model
        self.client: Client = create_client(
            url="YOUR_SUPABASE_URL",
            key="YOUR_SUPABASE_SERVICE_KEY"
        )

    async def create(self, data: Dict[str, Any]) -> Any:
        try:
            response = await self.client.from_(self.table_name).insert(data).execute()
            if response.error:
                raise HTTPException(status_code=400, detail=response.error.message)
            return self.response_model(**response.data[0])
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def read(self, id: str) -> Any:
        try:
            response = await self.client.from_(self.table_name).select("*").eq("id", id).execute()
            if response.error:
                raise HTTPException(status_code=400, detail=response.error.message)
            if not response.data:
                raise HTTPException(status_code=404, detail="Item not found")
            return self.response_model(**response.data[0])
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update(self, id: str, data: Dict[str, Any]) -> Any:
        try:
            response = await self.client.from_(self.table_name).update(data).eq("id", id).execute()
            if response.error:
                raise HTTPException(status_code=400, detail=response.error.message)
            return self.response_model(**response.data[0])
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete(self, id: str) -> None:
        try:
            response = await self.client.from_(self.table_name).delete().eq("id", id).execute()
            if response.error:
                raise HTTPException(status_code=400, detail=response.error.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))