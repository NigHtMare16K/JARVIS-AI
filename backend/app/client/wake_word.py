import logging

import numpy as np
import openwakeword
import pyaudio
from openwakeword.model import Model

from app.core.config import settings

logger = logging.getLogger(__name__)

CHUNK = 1280  # 80 ms at 16 kHz

_model: Model | None = None


def get_wake_word_model() -> Model:
    global _model
    if _model is None:
        openwakeword.utils.download_models()
        _model = Model(wakeword_models=[settings.WAKE_WORD])
        logger.info("Wake word model loaded: %s", settings.WAKE_WORD)
    return _model


def wait_for_wake_word(threshold: float | None = None) -> None:
    threshold = threshold if threshold is not None else settings.WAKE_WORD_THRESHOLD
    model = get_wake_word_model()

    audio = pyaudio.PyAudio()
    mic_stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=settings.SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("👂 Listening for wake word...")

    try:
        while True:
            audio_frame = np.frombuffer(
                mic_stream.read(CHUNK, exception_on_overflow=False),
                dtype=np.int16,
            )
            prediction = model.predict(audio_frame)

            score = prediction.get(settings.WAKE_WORD, 0)
            if score > threshold:
                print("🎯 Wake word detected!")
                return
    finally:
        mic_stream.stop_stream()
        mic_stream.close()
        audio.terminate()
