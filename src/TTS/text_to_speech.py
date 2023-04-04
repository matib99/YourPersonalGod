#TTS model - Real-Time-Voice-Cloning (RTVC)
#there should be cloned RTVC repo inside this directory
#and also sample wav file in this directory as well
#I tested it with pythons version 3.7.16
#before running the script it is necessary to download pretrained models, details are described in RTVC repository
import argparse
import soundfile as sf

import numpy as np
import torch
import sys
sys.path.append('./Real-Time-Voice-Cloning')
from synthesizer.inference import Synthesizer
from vocoder import inference as vocoder
from encoder import inference as encoder
from pathlib import Path


class Text_To_Speech():
    def __init__(self, model_path = "./Real-Time-Voice-Cloning/saved_models/default/"):

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
        return self.generated_wav

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


