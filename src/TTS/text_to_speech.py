#before running the script it is necessary to download pretrained models how its described in RTVC repository
import argparse
import soundfile as sf

import numpy as np
import torch
import sys, os


sys.path.insert(0, os.path.abspath("./TTS/RealTimeVoiceCloning"))
sys.path.insert(0, os.path.abspath("./TTS/RealTimeVoiceCloning/vocoder2"))
sys.path.insert(0, os.path.abspath("./TTS/RealTimeVoiceCloning/encoder2"))
sys.path.insert(0, os.path.abspath("./TTS/RealTimeVoiceCloning/synthesizer2"))

from TTS.RealTimeVoiceCloning.vocoder2 import inference as vocoder
from TTS.RealTimeVoiceCloning.encoder2 import inference as encoder
from TTS.RealTimeVoiceCloning.synthesizer2.inference import Synthesizer

# spec_synth = importlib.util.spec_from_file_location('synthesizer', rtvc + 'synthesizer2/inference.py')
# synthesizer = importlib.util.module_from_spec(spec_synth)
# spec_enc = importlib.util.spec_from_file_location('inference', rtvc + 'encoder2/inference.py')
# spec_voc = importlib.util.spec_from_file_location('vocoder', rtvc + 'vocoder2/inference.py')
# encoder = importlib.util.module_from_spec(spec_enc)
# vocoder = importlib.util.module_from_spec(spec_voc)



# Synthesizer = synthesizer.Synthesizer
# from TTS.RealTimeVoiceCloning.synthesizer.inference import Synthesizer
# from TTS.RealTimeVoiceCloning.encoder2 import inference as encoder
# from TTS.RealTimeVoiceCloning.vocoder2 import inference as vocoder

print('-------------------------------------------')
print(dir(encoder))
print('-------------------------------------------')

from pathlib import Path


def slerp_np(embed1, embed2, alpha):
    angle = np.arccos(np.dot(embed1, embed2))
    return (np.sin((1 - alpha) * angle) * embed1 + np.sin(alpha * angle) * embed2) / np.sin(angle)


class Text_To_Speech():
    def __init__(self, model_path = "./TTS/RealTimeVoiceCloning/saved_models/default/"):

        #parsing paths as arguments (it appears as though it is necessary)
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("-e", "--enc_model_fpath", type=Path,
                            default=str(model_path+"encoder.pt"),
                            help="Path to a saved encoder")
        parser.add_argument("-s", "--syn_model_fpath", type=Path,
                            default=str(model_path+"synthesizer.pt"),
                            help="Path to a saved synthesizer")
        parser.add_argument("-v", "--voc_model_fpath", type=Path,
                            default=str(model_path+"vocoder.pt"),
                            help="Path to a saved vocoder")
        parser.add_argument("--cpu", action="store_true", help=\
            "If True, processing is done on CPU, even when a GPU is available.")
        parser.add_argument("--no_sound", action="store_true", help=\
            "If True, audio won't be played.")
        parser.add_argument("--seed", type=int, default=None, help=\
            "Optional random number seed value to make toolbox deterministic.")
        args, unknown = parser.parse_known_args() #parsing only known lets jupyter notebook correctly interpret arguments
        arg_dict = vars(args)


        #Initialize synthesizer and load pre-trained models
        encoder.load_model(args.enc_model_fpath)
        vocoder.load_model(args.voc_model_fpath)

        self.synthesizer = Synthesizer(args.syn_model_fpath)
        
        #variable for loaded and generated wav files
        self.embedded_sample = None
        self.generated_wav = None

        #number of saved files (for naming purposes)
        self.num_generated=0

        if torch.cuda.is_available():
            print("Using GPU.\n")
        else:
            print("Using CPU, GPU not found.\n")

    def set_sample(self, sample_wav_path):
        preprocessed_wav = encoder.preprocess_wav(sample_wav_path)
        self.embedded_sample = encoder.embed_utterance(preprocessed_wav)
        print("file loaded and embeded")
        return

    def vocalize(self, text):
        #mel spectrogram (longer text is more efficient):
        specs = self.synthesizer.synthesize_spectrograms([text],[self.embedded_sample])
        spec = specs[0]
        #generating waveform:
        self.generated_wav = vocoder.infer_waveform(spec)
        #padding as a workaround for bug, cutting silence
        self.generated_wav = np.pad(self.generated_wav, (0, self.synthesizer.sample_rate), mode="constant")
        self.generated_wav = encoder.preprocess_wav(self.generated_wav)
        return

    def play_audio(self):
        import sounddevice as sd
        try:
            sd.stop()
            sd.play(self.generated_wav, self.synthesizer.sample_rate)
        except:
            raise
        return

    def save_audio(self,filename=None):
        if filename==None:
            filename = "output_%02d.wav" % self.num_generated
        else:
            filename=str(filename+".wav")
        sf.write(filename, self.generated_wav.astype(np.float32), self.synthesizer.sample_rate)
        self.num_generated += 1
        print("\nSaved output audio as %s\n\n" % filename)
        return

    def interpolate_embeddings(self, path1, path2, alpha):
        #alpha takes values 0<alpha<1
        #loading and embedding:
        wav1 = encoder.preprocess_wav(path1)
        wav2 = encoder.preprocess_wav(path2)

        first_sample = encoder.embed_utterance(wav1)
        second_sample = encoder.embed_utterance(wav2)

        #spherical interpolation slerp:
        interpolated_embedding = slerp_np(first_sample,second_sample,alpha)
        # L2-renormalisation (to eliminate possible numerical errors):
        interpolated_embedding = interpolated_embedding / np.linalg.norm(interpolated_embedding, 2)  

        self.embedded_sample = interpolated_embedding
        print("samples interpolated and embedded")
        return


