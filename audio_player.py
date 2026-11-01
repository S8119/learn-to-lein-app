from pathlib import Path

import numpy
import sounddevice
import wave


def play_wav(path):
    """Stops any current playback, then plays the WAV file."""
    stop_playback()
    path = Path(path)
    with wave.open(str(path), "rb") as wave_file:
        channels = wave_file.getnchannels()
        sample_width = wave_file.getsampwidth()
        sample_rate = wave_file.getframerate()
        raw = wave_file.readframes(wave_file.getnframes())

    if sample_width == 1:
        dtype = numpy.uint8
    elif sample_width == 2:
        dtype = numpy.int16
    elif sample_width == 4:
        dtype = numpy.int32
    else:
        raise ValueError(f"Unsupported sample width: {sample_width}")

    audio = numpy.frombuffer(raw, dtype=dtype)
    if channels > 1:
        audio = audio.reshape(-1, channels)
    sounddevice.play(audio, samplerate=sample_rate)


def stop_playback():
    sounddevice.stop()
