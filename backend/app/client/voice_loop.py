import requests
import urllib.parse
from app.client.voice_client import record_voice, play_audio, INPUT_FILE
from app.client.wake_word import wait_for_wake_word

SERVER_URL = "http://127.0.0.1:8000/voice/"
SESSION_ID = "user_1"
MAX_SILENT_TURNS = 2
EXIT_PHRASES = ["stop jarvis", "goodbye jarvis", "go to sleep"]


def converse_once():
    print("🎙️ Listening... speak now")
    record_voice()

    with open(INPUT_FILE, "rb") as f:
        files = {"audio": (INPUT_FILE, f, "audio/wav")}
        response = requests.post(
            SERVER_URL,
            files=files,
            data={"session_id": SESSION_ID}
        )

    if response.status_code != 200:
        print("❌ Server error:", response.status_code, response.text)
        return None

    with open("response.wav", "wb") as out:
        out.write(response.content)

    text = urllib.parse.unquote(response.headers.get("X-Transcribed-Text", ""))
    print(f"🗣️ You said: {text}")

    print("🔊 Playing response...")
    play_audio("response.wav")
    return text


def conversation_session():
    silence_count = 0
    while True:
        text = converse_once()

        if text is None:
            break

        if text.strip() == "":
            silence_count += 1
            if silence_count >= MAX_SILENT_TURNS:
                print("💤 No response — going back to sleep.")
                break
            continue
        silence_count = 0

        if any(phrase in text.lower() for phrase in EXIT_PHRASES):
            print("👋 Exit phrase detected — going back to sleep.")
            break


if __name__ == "__main__":
    print("🤖 Jarvis started! Press Ctrl+C to stop")
    try:
        while True:
            wait_for_wake_word()
            print("🎯 Awake — starting conversation")
            conversation_session()
    except KeyboardInterrupt:
        print("\n👋 Jarvis stopped.")