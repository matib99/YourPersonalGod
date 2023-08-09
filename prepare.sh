# conda environment (commented out)
if false; then
  conda create -n pipeline_env python==3.8
  conda activate pipeline_env
  pip install -r requirements.txt
  conda install -c conda-forge libstdcxx-ng
fi

# TTS Real-Time-Voice-Cloning
if ! test -d "./src/TTS/RealTimeVoiceCloning"; then
  cd ./src/TTS/
  git clone https://github.com/CorentinJ/Real-Time-Voice-Cloning.git RealTimeVoiceCloning
  cd ../..
fi

# changing Real-Time-Voice-Cloning files due to librosa version incompatibility and other, occasional incompatibilities
cd ./src/TTS/RealTimeVoiceCloning

if test -d "encoder" || test -d "vocoder" || test -d "synthesizer"; then
  mv vocoder vocoder2
  mv encoder encoder2
  mv synthesizer synthesizer2
fi

cd ./encoder2

sed '53,65c\
def wav_to_mel_spectrogram(wav):\
  """\
  Derives a mel spectrogram ready to be used by the encoder from a preprocessed audio waveform.\
  Note: this not a log-mel spectrogram.\
  """\
  frames = librosa.feature.melspectrogram(\
      y=wav,\
      sr=sampling_rate,\
      n_fft=int(sampling_rate * mel_window_length / 1000),\
      hop_length=int(sampling_rate * mel_window_step / 1000),\
      n_mels=mel_n_channels\
  )\
  return frames.astype(np.float32).T' audio.py > modified_file && mv modified_file audio.py

sed '42,42c\
        wav = librosa.resample(wav, orig_sr=source_sr, target_sr=sampling_rate)' audio.py > modified_file && mv modified_file audio.py

sed '2,2c\
from encoder2.params_data import *' audio.py > modified_file && mv modified_file audio.py


sed '1,5c\
from encoder2.params_data import *\
from encoder2.model import SpeakerEncoder\
from encoder2.audio import preprocess_wav   # We want to expose this function from here\
from matplotlib import cm\
from encoder2 import audio' inference.py > modified_file && mv modified_file inference.py

sed '1,2c\
from encoder2.params_model import *\
from encoder2.params_data import *' model.py > modified_file && mv modified_file model.py

cd ../vocoder2

sed '1,2c\
from vocoder2.models.fatchord_version import WaveRNN\
from vocoder2 import hparams as hp' inference.py > modified_file && mv modified_file inference.py

sed '4,4c\
import vocoder2.hparams as hp' audio.py > modified_file && mv modified_file audio.py

sed '1,1c\
from synthesizer2.hparams import hparams as _syn_hp' hparams.py > modified_file && mv modified_file hparams.py


cd ./models

sed '4,6c\
from vocoder2.distribution import sample_from_discretized_mix_logistic\
from vocoder2.display import *\
from vocoder2.audio import *' fatchord_version.py > modified_file && mv modified_file fatchord_version.py

cd ../../synthesizer2

sed '2,7c\
from synthesizer2 import audio\
from synthesizer2.hparams import hparams\
from synthesizer2.models.tacotron import Tacotron\
from synthesizer2.utils.symbols import symbols\
from synthesizer2.utils.text import text_to_sequence\
from vocoder2.display import simple_table' inference.py > modified_file && mv modified_file inference.py

cd ./utils

sed '1,2c\
from synthesizer2.utils.symbols import symbols\
from synthesizer2.utils import cleaners' text.py > modified_file && mv modified_file text.py

sed '14,14c\
from synthesizer2.utils.numbers import normalize_numbers' cleaners.py > modified_file && mv modified_file cleaners.py

cd ../../


#downloading tts models
mkdir -p saved_models/default && cd ./saved_models/default

if ! test -f "encoder.pt" && ! test -f "synthesizer.pt" && ! test -f "vocoder.pt"; then
  wget -O encoder.pt "https://drive.google.com/uc?export=download&id=1q8mEGwCkFy23KZsinbuvdKAQLqNKbYf1"
  wget -O synthesizer.pt "https://drive.google.com/u/0/uc?id=1EqFMIbvxffxtjiVrtykroF6_mUh-5Z3s&export=download&confirm=t"
  wget -O vocoder.pt "https://drive.google.com/uc?export=download&id=1cf2NO6FtI0jDuy8AV3Xgn6leO6dHjIgu"
fi


cd ../..
