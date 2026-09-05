import requests
from app.client.voice_client import record_voice, play_audio, INPUT_FILE

SERVER_URL = "http://127.0.0.1:8000/voice/"

def run_once():
    print("🎙️ Listening... speak now")
    record_voice()

    with open(INPUT_FILE, "rb") as f:
        files = {"audio": (INPUT_FILE, f, "audio/wav")}
        response = requests.post(SERVER_URL, files=files)

    if response.status_code == 200:
        output_path = "response.wav"
        with open(output_path, "wb") as out:
            out.write(response.content)
        print("🔊 Playing response...")
        play_audio(output_path)
    else:
        print("❌ Server error:", response.status_code, response.text)

if __name__ == "__main__":
    run_once()