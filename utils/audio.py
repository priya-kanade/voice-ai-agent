import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

recording = []
is_recording = False

def start_recording(fs=16000):   # 🔥 LOWER SAMPLE RATE (better for speech)
    global recording, is_recording
    recording = []
    is_recording = True

    def callback(indata, frames, time, status):
        if is_recording:
            recording.append(indata.copy())

    stream = sd.InputStream(callback=callback, channels=1, samplerate=fs)
    stream.start()
    return stream

def stop_recording(stream, filename="input.wav", fs=16000):
    global is_recording
    is_recording = False
    stream.stop()
    stream.close()

    audio = np.concatenate(recording, axis=0)

    # 🔥 Normalize audio (IMPORTANT)
    audio = audio / np.max(np.abs(audio))

    write(filename, fs, audio)

    return filename