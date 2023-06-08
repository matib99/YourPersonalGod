 
# YourPersonalGod

A repository for the AI Algorythmic Art project. It's goal is to produce interactive AI god in your image.

## Components (subject to change):

* Visual
  * StyleGan finetuned to generate slavic god in your image
* Audio-Linguistic
  * [Real-Time-Voice-Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning) for generating speech in your own voice
  * [Whisper](https://github.com/openai/whisper) - for transcribing your speech
  * [llama](https://pypi.org/project/llama-cpp-python/) compatible model - for generating answers

## Installation (works at least on linux with anaconda installed)

* To install requirements it is preferred to create separate conda environment with python version 3.8, for example by using snippet (if not all requirements work out of the box you might need to install every library separately for some reason):

  ```bash
  conda create -n pipeline_env python==3.8
  conda activate pipeline_env
  pip install -r requirements.txt
  ```
* Sometimes required version of Gnu C++ Library (GLIBCXX) isn't supported by libstdc++ version installed by default with python 3.8. Entering following snippet solves the problem:

  ```bash
  conda install -c conda-forge libstdcxx-ng
  ```
* Real-Time-Voice-Cloning has to be cloned into directory ./src/TTS/ with following snippet:

  ```bash
  cd ./src/TTS/
  git clone https://github.com/CorentinJ/Real-Time-Voice-Cloning.git
  cd ../..
  ```
* Then due to librosa incompatibility you will need to change function "wav_to_mel_spectrogram(wav)" and variable "wav=librosa.resample(...)"in ./src/TTS/Real-Time-Voice-Cloning/encoder/audio.py according to [this thread](https://github.com/PaddlePaddle/PaddleSpeech/issues/1426). Correct versions look like following:

  ```python
  def wav_to_mel_spectrogram(wav):
    frames = librosa.feature.melspectrogram(
        y=wav,
        sr=sampling_rate,
        n_fft=int(sampling_rate * mel_window_length / 1000),
        hop_length=int(sampling_rate * mel_window_step / 1000),
        n_mels=mel_n_channels
    )
    return frames.astype(np.float32).T
  ```

  and
  ```python
  wav = librosa.resample(wav, orig_sr=source_sr, target_sr=sampling_rate)
  ```
* then you will need to download 8-bit quantized model (with .bit extension) to ./models/ directory. models are available in user [huggingface](huggingface.co/models?search=vicuna) repositories (I'm working with [this](https://huggingface.co/CRD716/ggml-vicuna-1.1-quantized/blob/main/ggml-vicuna-13B-1.1-q4_0.bin)), you have to find a model trained after approximately 19.05.2023, older ones tend to not be compatible with the latest llama.cpp library, so to use older versions you will need to downgrade llama_cpp_python library.
* you have to first run RTVC demo file as described [here](https://github.com/CorentinJ/Real-Time-Voice-Cloning) in order to download a working model. It just requires you to run demo_cli.py file in RTVC directory.
* you may have to change default_mic variable when calling class VoiceInput in pipeline_demo.py file (line 14) to your desired input audio server name (most likely to 'pulse'), You also have to change model path in pipeline_demo.py file to match your LLM.

## Repository structure

* ./models/ is for storing Large Language Models (LLM), they have to be 8-bit quantized and compatible with current llama_cpp_python version (I was working with version 0.1.54)
* ./src/ holds pipeline_demo and folders with used classes and their testfiles. Additionaly in ./src/Conversation/ there is prompt.txt file that holds entire conversation prompt for LLM. In TTS you have to clone RTVC repo (and change some of its functions as described in previous section). Both samples and outpust are by default stored in ./src/
