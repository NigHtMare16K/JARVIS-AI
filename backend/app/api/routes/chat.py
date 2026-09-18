import logging

from fastapi import APIRouter, HTTPException

from app.agent.graph import run_agent
from app.schemas.chat import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["LLM Chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    try:
        answer = run_agent(payload.message, payload.session_id)
        return ChatResponse(answer=answer)
    except Exception as exc:
        logger.exception("Chat endpoint error")
        raise HTTPException(status_code=500, detail="Chat failed. Please try again.") from exc
