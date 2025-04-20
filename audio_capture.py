import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=CHUNK)

def get_audio_chunk():
    """Reads raw audio chunk from mic."""
    return stream.read(CHUNK, exception_on_overflow=False)

def close_audio():
    """Stops and closes the audio stream/device."""
    stream.stop_stream()
    stream.close()
    p.terminate()