from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
import tempfile
import urllib.parse

from app.services.voice_service import process_voice

router = APIRouter(prefix="/voice", tags=["Voice Assistant"])


@router.post("/")
def voice(audio: UploadFile = File(...), session_id: str = Form(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        temp.write(audio.file.read())
        audio_path = temp.name

    result = process_voice(audio_path, session_id)

    return FileResponse(
        result["audio"],
        media_type="audio/wav",
        filename="jarvis_response.wav",
        headers={"X-Transcribed-Text": urllib.parse.quote(result["text"])}
    )