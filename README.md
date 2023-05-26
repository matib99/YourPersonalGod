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

* To install requirements it is preferred to create separate conda environment with python version 3.8 using snippet (if not all requirements work out of the box you might need to install every library separately for some reason):

  ```bash
  conda create -n YourEnv python==3.8
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
* Then due to librosa incompatibility you will need to change two functions  (librosa.feature.melspectrogram(...) and librosa.resample(...))in ./src/TTS/Real-Time-Voice-Cloning/vocoder/audio.py according to [this thread](https://github.com/PaddlePaddle/PaddleSpeech/issues/1426). Correct versions look like following:

  ```python
  librosa.feature.melspectrogram(*, y=None, sr=22050, S=None, n_fft=2048, hop_length=512, win_length=None, window='hann', center=True, pad_mode='constant', power=2.0, **kwargs)
  ```

  and
  ```python
  librosa.resample(y, *, orig_sr, target_sr, res_type='soxr_hq', fix=True, scale=False, axis=-1, **kwargs)
  ```
* then you will need to download 8-bit quantized model (with .bit extension) to ./models/ directory. models are available in user [huggingface](huggingface.co/models?search=vicuna) repositories (I'm working with [this](https://huggingface.co/CRD716/ggml-vicuna-1.1-quantized/blob/main/ggml-vicuna-13B-1.1-q4_0.bin)), you have to find a model trained after approximately 19.05.2023, older ones tend to not be compatible with the latest llama.cpp library, so to use older versions you will need to downgrade llama_cpp_python library.
* you have to first run RTVC demo file as described [here](https://github.com/CorentinJ/Real-Time-Voice-Cloning) in order to download a working model
* you may have to change default_mic variable when calling class VoiceInput in pipeline_demo.py file (line 14) to your desired input audio server name (most likely to 'pulse').

## Repository structure

* ./models/ is for storing Large Language Models (LLM), they have to be 8-bit quantized and compatible with current llama_cpp_python version (I was working with version 0.1.54)
* ./src/ holds pipeline_demo and folders with used classes and their testfiles. Additionaly in ./src/Conversation/ there is prompt.txt file that holds entire conversation prompt for LLM. In TTS you have to clone RTVC repo (and change some of its functions as described in previous section). Both samples and outpust are by default stored in ./src/