from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.models.codex import CodexRequest, CodexResponse
from app.services.llm_service import LLMService
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/codex/generate", response_model=CodexResponse)
async def generate_codex_response(
    request: CodexRequest,
    current_user: User = Depends(get_current_user)
) -> CodexResponse:
    try:
        llm_service = LLMService()
        result = await llm_service.generate(request.prompt)
        return CodexResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))