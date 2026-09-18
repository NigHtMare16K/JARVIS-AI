import logging
import time
import urllib.parse

import requests

from app.client.voice_client import INPUT_FILE, play_audio, record_voice
from app.client.wake_word import wait_for_wake_word
from app.core.config import settings

logger = logging.getLogger(__name__)

SERVER_URL = "http://127.0.0.1:8000/voice/"
SESSION_ID = "user_1"
EXIT_PHRASES = ["stop jarvis", "goodbye jarvis", "go to sleep", "go to sleep jarvis"]


def converse_once() -> str | None:
    print("🎙️ Listening... speak naturally")
    try:
        got_speech = record_voice(INPUT_FILE)
    except RuntimeError as exc:
        print(f"❌ Microphone error: {exc}")
        return None

    if not got_speech:
        print("🔇 No speech detected.")
        return ""

    try:
        with open(INPUT_FILE, "rb") as f:
            files = {"audio": (INPUT_FILE, f, "audio/wav")}
            response = requests.post(
                SERVER_URL,
                files=files,
                data={"session_id": SESSION_ID},
                timeout=120,
            )
    except requests.RequestException as exc:
        print(f"❌ Server connection error: {exc}")
        return None

    if response.status_code != 200:
        print("❌ Server error:", response.status_code, response.text)
        return None

    with open("response.wav", "wb") as out:
        out.write(response.content)

    text = urllib.parse.unquote(response.headers.get("X-Transcribed-Text", ""))
    answer = urllib.parse.unquote(response.headers.get("X-Answer-Text", ""))
    print(f"🗣️ You said: {text}")
    if answer:
        print(f"🤖 Jarvis: {answer}")

    print("🔊 Playing response...")
    try:
        play_audio("response.wav")
    except RuntimeError as exc:
        print(f"⚠️ Playback issue: {exc}")

    return text


def conversation_session() -> None:
    silence_count = 0
    session_start = time.time()
    max_idle = settings.CONVERSATION_IDLE_TIMEOUT_SEC

    while True:
        if time.time() - session_start > max_idle:
            print("💤 Conversation idle timeout — going back to sleep.")
            break

        text = converse_once()

        if text is None:
            break

        if text.strip() == "":
            silence_count += 1
            if silence_count >= settings.MAX_SILENT_TURNS:
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
