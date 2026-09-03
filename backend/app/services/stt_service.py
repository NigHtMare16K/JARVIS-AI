from faster_whisper import WhisperModel

# Load Whisper
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def transcribe_audio(audio_path: str) ->str:
    segments, info = model.transcribe(audio_path)
    return " ".join(segment.text for segment in segments).strip()

