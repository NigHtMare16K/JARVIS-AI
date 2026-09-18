"""Assistant status and session endpoints for the frontend."""

from fastapi import APIRouter

from app.rag.active_window import get_active_pdf, get_active_window_title
from app.services.llm_service import store

router = APIRouter(prefix="/assistant", tags=["Assistant"])


@router.get("/status")
def assistant_status():
    return {
        "status": "online",
        "active_window": get_active_window_title(),
        "active_pdf": get_active_pdf(),
        "active_sessions": len(store),
    }


@router.get("/health")
def health():
    return {"status": "ok"}
