import pyaudio
import wave
from ctypes import *
from contextlib import contextmanager
import time

# private functions
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

# function for recording sample from voice that will be used for cloning
def VoiceRecord(waitfor=3, seconds=7, filename="sample.wav"):
    chunk = 1024  
    sample_format = pyaudio.paInt16  
    # Mono channel
    channels = 1
    # 24 kHz
    fs = 24000  
    # Recording duration
    seconds = 7
    with noalsaerr():
        p = pyaudio.PyAudio()
        time.sleep(3)
        print('Recording')
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames


        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)


        stream.stop_stream()
        stream.close()
        p.terminate()

        print('Finished recording')

        # Saving to wav
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
