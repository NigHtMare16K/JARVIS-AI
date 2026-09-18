import logging
import os
import tempfile
import urllib.parse

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse

from app.services.voice_service import process_voice

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/voice", tags=["Voice Assistant"])


@router.post("/")
def voice(audio: UploadFile = File(...), session_id: str = Form(...)):
    audio_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
            temp.write(audio.file.read())
            audio_path = temp.name

        result = process_voice(audio_path, session_id)

        return FileResponse(
            result["audio"],
            media_type="audio/wav",
            filename="jarvis_response.wav",
            headers={
                "X-Transcribed-Text": urllib.parse.quote(result["text"] or ""),
                "X-Answer-Text": urllib.parse.quote(result["answer"] or ""),
            },
        )
    except Exception as exc:
        logger.exception("Voice endpoint error")
        return JSONResponse(
            status_code=500,
            content={"detail": "Voice processing failed. Please try again."},
        )
    finally:
        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except OSError:
                pass
