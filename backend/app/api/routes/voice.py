import os
import tempfile

from fastapi import APIRouter, UploadFile, File

from app.services.stt_service import transcribe_audio
from app.services.llm_service import generate_response
from app.services.tts_service import text_to_speech


router = APIRouter(prefix="/voice", tags=["Voice Assistant"])


@router.post("/")
async def voice(audio: UploadFile = File(...)):

    # Save uploaded audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        temp.write(await audio.read())
        audio_path = temp.name

    # 1. Speech → Text
    text = transcribe_audio(audio_path)

    # 2. Text → LLM response
    response = generate_response(text)
    answer = response["answer"]

    # 3. Text → Speech
    output_path = text_to_speech(answer)

    # Clean up input file
    os.remove(audio_path)

    return {
        "transcript": text,
        "answer": answer,
        "audio_file": output_path
    }