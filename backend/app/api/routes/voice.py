from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
import tempfile

from app.services.voice_service import process_voice

router = APIRouter(
    prefix="/voice",
    tags=["Voice Assistant"]
)


@router.post("/")
def voice(audio: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        temp.write(audio.file.read())
        audio_path = temp.name

    result = process_voice(audio_path)

    return FileResponse(
        result["audio"],
        media_type="audio/wav",
        filename="jarvis_response.wav"
    )