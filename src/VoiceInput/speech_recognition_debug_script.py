import speech_recognition as sr


mic_name='pulse'

recorder = sr.Recognizer()
recorder.energy_threshold=1000
recorder.pause_threshold = 1.5


for index, name in enumerate(sr.Microphone.list_microphone_names()):
                    if mic_name in name:
                        source = sr.Microphone(
                            sample_rate=16000, device_index=index)
                        break


with source:
            recorder.adjust_for_ambient_noise(source)
            print(" Recording:")
            data = recorder.listen(source, phrase_time_limit=5)

print("voice recorded")

transcription=recorder.recognize_whisper(data, "small.en")

print(f'transcription: {transcription}')
