from app.services.stt_service import transcribe_audio
from app.services.llm_service import generate_response
from app.services.tts_service import text_to_speech
from app.agent.graph import run_agent

def process_voice(audio_path: str, session_id: str):

    # 1. Speech → Text
    text = transcribe_audio(audio_path)

    # 2. Text → LLM Response
    answer = run_agent(text, session_id)

    # 3. Text → Speech
    output_path = text_to_speech(answer)

    return {
        "text": text,
        "answer": answer,
        "audio": output_path
    }