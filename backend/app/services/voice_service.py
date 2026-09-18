import logging
import os
import uuid

from app.agent.graph import run_agent
from app.services.stt_service import transcribe_audio
from app.services.tts_service import text_to_speech

logger = logging.getLogger(__name__)


def process_voice(audio_path: str, session_id: str) -> dict:
    """STT → LangGraph agent → TTS pipeline with error handling."""
    text = ""
    answer = ""

    try:
        text = transcribe_audio(audio_path)
    except Exception as exc:
        logger.exception("STT failed")
        answer = "I couldn't understand the audio. Please try again."
        text = ""

    if not text.strip():
        if not answer:
            answer = "I didn't catch that. Could you repeat?"
    else:
        try:
            answer = run_agent(text, session_id)
        except Exception as exc:
            logger.exception("Agent failed")
            answer = "I'm having trouble thinking right now. Please try again."

    output_path = f"output_{uuid.uuid4().hex[:8]}.wav"
    try:
        text_to_speech(answer, output_path)
    except Exception as exc:
        logger.exception("TTS failed")
        # Fallback: create minimal silent wav or reuse empty
        answer = f"{answer} (Speech synthesis unavailable.)"
        try:
            text_to_speech("Sorry, I couldn't speak the response.", output_path)
        except Exception:
            output_path = audio_path  # last resort

    return {
        "text": text,
        "answer": answer,
        "audio": output_path,
    }
