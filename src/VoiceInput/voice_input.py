import argparse
import io
import os
import speech_recognition as sr
import whisper
import torch

from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep
from sys import platform


class VoiceInput():
    def __init__(self, whisper_model='small', non_english=False, energy_treshold=1000, default_mic='pulse', record_timeout=2, phrase_timeout=3):
        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = energy_treshold
        self.dynamic_energy_treshold = True

        self.recorder.pause_threshold = 1.5

        if 'linux' in platform:
            mic_name = default_mic
            if not mic_name or mic_name == 'list':
                print("Available microphone devices are: ")
                for index, name in enumerate(sr.Microphone.list_microphone_names()):
                    print(f"Microphone with name \"{name}\" found")
                return
            else:
                for index, name in enumerate(sr.Microphone.list_microphone_names()):
                    if mic_name in name:
                        source = sr.Microphone(
                            sample_rate=16000, device_index=index)
                        break
        else:
            source = sr.Microphone(sample_rate=16000)

        self.source = source
        self.record_timeout = record_timeout
        self.phrase_timeout = phrase_timeout

        model = whisper_model
        if model != "large" and not non_english:
            model = model + ".en"
        self.audio_model = model 

        with source:
            self.recorder.adjust_for_ambient_noise(source)
    
    def get_phrase(self):
        with self.source:
            data = self.recorder.listen(self.source)
        transcription=self.recorder.recognize_whisper(data, self.audio_model)
        return transcription
# self.energy_threshold = 300  # minimum audio energy to consider for recording
# self.dynamic_energy_threshold = True
# self.dynamic_energy_adjustment_damping = 0.15
# self.dynamic_energy_ratio = 1.5
# self.pause_threshold = 0.8  # seconds of non-speaking audio before a phrase is considered complete
# self.operation_timeout = None  # seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout

# self.phrase_threshold = 0.3  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
# self.non_speaking_duration = 0.5  # seconds of non-speaking audio to keep on both sides of the recording