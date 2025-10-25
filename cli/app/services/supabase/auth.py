from __future__ import annotations


class SupabaseAuth:
    """Placeholder for Supabase auth client.

    Implement login/logout with supabase-py later if desired.
    """

    async def login(self, email: str, password: str) -> str:
        raise NotImplementedError

    async def logout(self, user_id: str) -> None:
        raise NotImplementedError

