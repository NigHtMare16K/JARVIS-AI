from app.services.stt_service import transcribe_audio
from app.services.llm_service import generate_response
from app.services.tts_service import text_to_speech


def process_voice(audio_path: str):

    # 1. Speech → Text
    text = transcribe_audio(audio_path)

    # 2. Text → LLM Response
    response = generate_response(text)

    # 3. Text → Speech
    output_path = text_to_speech(response["answer"])

    # return {
    #     "text": text,
    #     "answer": response["answer"],
    #     "audio": audio_output
    # }

    return output_path