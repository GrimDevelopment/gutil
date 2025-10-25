from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.app.models.user import User
from backend.app.services.supabase_auth import SupabaseAuthService

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    try:
        auth_service = SupabaseAuthService()
        access_token = await auth_service.login(request.email, request.password)
        return LoginResponse(access_token=access_token, token_type="bearer")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    try:
        auth_service = SupabaseAuthService()
        await auth_service.logout(current_user.id)
        return {"detail": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))