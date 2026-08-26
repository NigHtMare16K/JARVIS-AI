# from faster_whisper import WhisperModel

# model = WhisperModel(
#     "base",
#     device="cpu",
#     compute_type="int8"
# )

# segmnents, info = model.transcribe("test.wav")

# print("Detected Language:", info.language)

# for segmnent in segmnents:
#     print(segmnent.text)

import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

# Recording settings
sample_rate = 16000
duration = 5

print("🎤 Speak now...")

audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)

sd.wait()

write("recording.wav", sample_rate, audio)

print("✅ Recording saved.")

# Load Whisper
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("🧠 Transcribing...")

segments, info = model.transcribe("recording.wav")

print("\nYou said:")

for segment in segments:
    print(segment.text)