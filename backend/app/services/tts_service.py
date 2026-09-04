import os
import wave
from piper import PiperVoice

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR, "..", "..", "models", "en_US-lessac-medium.onnx"
)

voice = PiperVoice.load(MODEL_PATH)


def text_to_speech(text: str, output_path: str = "output.wav"):
    with wave.open(output_path, "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    return output_path