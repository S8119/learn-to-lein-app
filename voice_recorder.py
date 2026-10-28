import sounddevice
import numpy
import wave

# --- Configuration ---
SAMPLE_RATE = 44100          # samples captured per second (44.1kHz, CD quality)
CHANNELS = 1                 # 1 = mono, sufficient for a single voice

SAMPLE_WIDTH_BYTES = 2                          # 16-bit audio = 2 bytes per sample
MAX_INT16_VALUE = numpy.iinfo(numpy.int16).max

class RecordingState:
    """
    Represents the current recording status.
    One instance of this is the single source of truth for the
    whole app, held by main.py (on root), and threaded through
    functions explicitly.
    """

    def __init__(self, is_recording=False, stream=None, recording_frames=None):
        self.is_recording = is_recording
        self.stream = stream
        if recording_frames is not None:
            self.recording_frames = recording_frames
        else:
            self.recording_frames = []

def start_recording():
    """
    Begins recording the boy's voice.
    Call this when the 'Start Recording' button is pressed.
    """
    recording_frames = []

    def audio_callback(indata, _frames, _time, status):
        """
        Called automatically by sounddevice for every small chunk
        of audio while recording is active.
        Because this function is defined inside start_recording(),
        it has direct access to the recording_frames list above
        without needing a global variable.
        """
        if status:
            print("Recording status warning:", status)
        recording_frames.append(indata.copy())

    stream = sounddevice.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        callback=audio_callback
    )
    stream.start()
    is_recording = True

    print("Recording started...")
    return stream, recording_frames, is_recording


def stop_recording(stream, recording_frames, is_recording, output_filename):
    """
    Ends the recording and saves it to OUTPUT_FILENAME.
    Call this when the 'Stop Recording' button is pressed.
    Takes in the same (stream, recording_frames, is_recording) tuple
    that start_recording() returned.
    """
    if not is_recording:
        print("Not currently recording — ignoring stop_recording() call.")
        success = False

    else:
        stream.stop()
        stream.close()
        is_recording = False

        if len(recording_frames) == 0:
            print("No audio was captured.")
            success = False

        else:
            audio_data = numpy.concatenate(recording_frames, axis=0)
            _save_to_wav(audio_data, output_filename)
            print(f"Recording stopped and saved to '{output_filename}'.")
            success = True

    return success


def _save_to_wav(audio_data, output_filename):
    """
    Internal helper: writes a numpy float32 audio array
    to a standard 16-bit PCM .wav file.
    """
    # Convert from float32 [-1.0, 1.0] to int16 PCM
    audio_int16 = numpy.int16(
        numpy.clip(audio_data, -1.0, 1.0) * MAX_INT16_VALUE
    )

    with wave.open(output_filename, 'wb') as wave_file:
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(SAMPLE_WIDTH_BYTES)
        wave_file.setframerate(SAMPLE_RATE)
        wave_file.writeframes(audio_int16.tobytes())