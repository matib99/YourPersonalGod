from text_to_speech import Text_To_Speech
import sys
sys.path.append('./Real-Time-Voice-Cloning')


TTS = Text_To_Speech()
TTS.set_sample('./sample.wav')
TTS.vocalize('this is example text that will be vocalised with cloned voice')
try: 
    TTS.play_audio()
    TTS.save_audio()
except:
    TTS.save_audio()
#generating this on CPU takes around 10 seconds, length doesn't scale linearly, device is more efficient with longer text.