import os
import wave
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
from groq import Groq
from piper import PiperVoice
from dotenv import load_dotenv


# =========================
# CONFIGURATION
# =========================

SAMPLE_RATE = 16000
DURATION = 5

WHISPER_MODEL = "base"
GROQ_MODEL = "openai/gpt-oss-120b"
PIPER_MODEL = "en_US-lessac-medium.onnx"

load_dotenv()

# =========================
# LOAD MODELS
# =========================

print("Loading Whisper...")
whisper = WhisperModel(
    WHISPER_MODEL,
    device="cpu",
    compute_type="int8"
)

print("Loading Piper...")
voice = PiperVoice.load(PIPER_MODEL)

print("Connecting to Groq...")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("✅ Everything loaded!\n")


# =========================
# RECORD VOICE
# =========================

print("🎤 Speak now...")

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16"
)

sd.wait()

write("recording.wav", SAMPLE_RATE, audio)

print("✅ Recording saved.")


# =========================
# WHISPER
# =========================

print("🧠 Transcribing...")

segments, info = whisper.transcribe("recording.wav")

text = ""

for segment in segments:
    text += segment.text

text = text.strip()

print("\n👤 You:")
print(text)


# =========================
# GROQ
# =========================

print("\n🤖 Thinking...")

response = client.chat.completions.create(
    model=GROQ_MODEL,
    messages=[
        {
            "role": "system",
            "content": "You are Jarvis, a helpful and concise AI voice assistant."
        },
        {
            "role": "user",
            "content": text
        }
    ]
)

answer = response.choices[0].message.content

print("\n🤖 Jarvis:")
print(answer)


# =========================
# PIPER TTS
# =========================

print("\n🔊 Generating voice...")

with wave.open("response.wav", "wb") as wav_file:
    voice.synthesize_wav(answer, wav_file)

print("✅ Voice generated: response.wav")


# =========================
# PLAY AUDIO
# =========================

print("🔊 Playing response...")

import soundfile as sf

audio_data, samplerate = sf.read("response.wav")

sd.play(audio_data, samplerate)
sd.wait()

print("\n✅ Done!")