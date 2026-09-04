from fastapi import APIRouter
from app.services.llm_service import generate_response
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(
    prefix="/chat",
    tags = ["LLM Chat"]
)

@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    response = generate_response(payload.message)

    return ChatResponse(answer = response["answer"])