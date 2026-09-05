import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write

SAMPLE_RATE = 16000
DURATION = 5

INPUT_FILE = "input.wav"

def record_voice():
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    write(INPUT_FILE, SAMPLE_RATE, audio)

def play_audio(output_path: str):
    audio_data, samplerate = sf.read(output_path)

    sd.play(audio_data, samplerate)

    sd.wait()