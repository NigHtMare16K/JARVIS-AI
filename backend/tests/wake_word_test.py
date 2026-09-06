import pyaudio
import numpy as np
import openwakeword
from openwakeword.model import Model

openwakeword.utils.download_models()

model = Model(wakeword_models=["hey_jarvis"])

CHUNK = 1280  # 80ms at 16kHz
audio = pyaudio.PyAudio()
mic_stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=CHUNK
)

print("👂 Listening for wake word...")

while True:
    audio_frame = np.frombuffer(mic_stream.read(CHUNK), dtype=np.int16)
    prediction = model.predict(audio_frame)

    if prediction["hey_jarvis"] > 0.5:
        print("🎯 Wake word detected!")
        # trigger your existing record_voice() → process_voice() pipeline here