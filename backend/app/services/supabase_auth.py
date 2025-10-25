from fastapi import HTTPException
from supabase import create_client, Client
from typing import Any, Dict

class SupabaseAuthService:
    def __init__(self, supabase_url: str, supabase_key: str) -> None:
        self.supabase: Client = create_client(supabase_url, supabase_key)

    async def sign_up(self, email: str, password: str) -> Dict[str, Any]:
        try:
            response = await self.supabase.auth.sign_up(email=email, password=password)
            return response
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        try:
            response = await self.supabase.auth.sign_in(email=email, password=password)
            return response
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def sign_out(self) -> None:
        try:
            await self.supabase.auth.sign_out()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_user(self) -> Dict[str, Any]:
        user = self.supabase.auth.user()
        if user is None:
            raise HTTPException(status_code=401, detail="User not authenticated")
        return user