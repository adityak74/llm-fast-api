from fastapi import APIRouter
from app.models.chat import ChatCompletionRequest, ChatCompletionResponse
from app.services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()

@router.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(request: ChatCompletionRequest):
    content = await llm_service.create_chat_completion(request.model_dump())
    return ChatCompletionResponse(content=content) 