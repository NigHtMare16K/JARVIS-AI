import logging

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

from app.core.config import settings

logger = logging.getLogger(__name__)

SAMPLE_RATE = settings.SAMPLE_RATE
INPUT_FILE = "input.wav"


def _rms_energy(chunk: np.ndarray) -> float:
    if chunk.size == 0:
        return 0.0
    normalized = chunk.astype(np.float32) / 32768.0
    return float(np.sqrt(np.mean(normalized ** 2)))


def record_voice_vad(
    output_path: str = INPUT_FILE,
    sample_rate: int | None = None,
    speech_threshold: float | None = None,
    silence_duration: float | None = None,
    max_duration: float | None = None,
    pre_speech_buffer: float | None = None,
) -> bool:
    """
    Record audio using energy-based VAD.
    Waits for speech, records until silence, returns True if speech captured.
    """
    sr = sample_rate or settings.SAMPLE_RATE
    threshold = speech_threshold if speech_threshold is not None else settings.SPEECH_ENERGY_THRESHOLD
    silence_sec = silence_duration if silence_duration is not None else settings.SILENCE_DURATION_SEC
    max_sec = max_duration if max_duration is not None else settings.MAX_UTTERANCE_DURATION_SEC
    pre_buffer_sec = pre_speech_buffer if pre_speech_buffer is not None else settings.PRE_SPEECH_BUFFER_SEC

    chunk_duration = 0.05  # 50 ms chunks
    chunk_samples = int(sr * chunk_duration)
    silence_chunks_needed = int(silence_sec / chunk_duration)
    max_chunks = int(max_sec / chunk_duration)
    pre_buffer_chunks = int(pre_buffer_sec / chunk_duration)

    ring_buffer: list[np.ndarray] = []
    recorded: list[np.ndarray] = []
    silent_count = 0
    speech_started = False
    chunk_count = 0

    logger.info("VAD listening (threshold=%.4f, silence=%.1fs)", threshold, silence_sec)

    try:
        with sd.InputStream(samplerate=sr, channels=1, dtype="int16") as stream:
            while chunk_count < max_chunks:
                chunk, _overflowed = stream.read(chunk_samples)
                chunk_arr = chunk.flatten()
                chunk_count += 1

                energy = _rms_energy(chunk_arr)
                is_speech = energy > threshold

                if not speech_started:
                    ring_buffer.append(chunk_arr)
                    if len(ring_buffer) > pre_buffer_chunks:
                        ring_buffer.pop(0)

                    if is_speech:
                        speech_started = True
                        recorded.extend(ring_buffer)
                        ring_buffer.clear()
                        silent_count = 0
                else:
                    recorded.append(chunk_arr)
                    if is_speech:
                        silent_count = 0
                    else:
                        silent_count += 1
                        if silent_count >= silence_chunks_needed:
                            break

    except Exception as exc:
        logger.exception("Microphone error during VAD recording")
        raise RuntimeError(f"Microphone error: {exc}") from exc

    if not speech_started or not recorded:
        logger.info("No speech detected")
        return False

    audio = np.concatenate(recorded)
    write(output_path, sr, audio)
    duration = len(audio) / sr
    logger.info("Recorded %.1fs of speech", duration)
    return True


def record_voice(output_path: str = INPUT_FILE) -> bool:
    """Record one utterance using VAD. Returns True if speech was captured."""
    return record_voice_vad(output_path=output_path)


def play_audio(output_path: str) -> None:
    import soundfile as sf

    try:
        audio_data, samplerate = sf.read(output_path)
        sd.play(audio_data, samplerate)
        sd.wait()
    except Exception as exc:
        logger.exception("Audio playback failed")
        raise RuntimeError(f"Playback error: {exc}") from exc
