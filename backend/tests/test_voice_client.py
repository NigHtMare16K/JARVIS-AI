import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write

from app.services.voice_service import process_voice


SAMPLE_RATE = 16000
DURATION = 5

INPUT_FILE = "input.wav"


# 1. Record audio
print("🎤 Speak now...")

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16"
)

sd.wait()

write(INPUT_FILE, SAMPLE_RATE, audio)

print("✅ Recording saved.")


# 2. Process voice
output_path = process_voice(INPUT_FILE)

print("🔊 Playing response...")


# 3. Play generated audio
audio_data, samplerate = sf.read(output_path)

sd.play(audio_data, samplerate)

sd.wait()

print("✅ Done")