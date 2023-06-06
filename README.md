# StyleGAN-Human:  A Data-Centric Odyssey of Human Generation
fork from: https://github.com/stylegan-human/StyleGAN-Human

## Data Download
[God-Human Dataset](https://drive.google.com/drive/folders/1Tl5KorGxcwABZjwC0mp9FhfAKb-UMeZw?usp=sharing)

## Model download
StyleGAN2 Pretrained Human Model: [stylegan_human_v2_1024.pkl](https://drive.google.com/file/d/1FlAb1rYa0r_--Zj_ML8e6shmaF28hQb5/view?usp=sharing)

StyleGAN2 Pretrained God-Human Model: [god-human-model.pkl](https://drive.google.com/file/d/1NLVeo256NT2g4pIi8JDdp5kgbQhIrr5B/view?usp=sharing)

Place above models in `pretrained_models` dir. 

## Usage

### System requirements
* The original code base is [stylegan2-ada (pytorch)](https://github.com/NVlabs/stylegan2-ada-pytorch), released by NVidia

* We tested in Python 3.8.3 and PyTorch 1.8.1 with CUDA 12.1. (See https://pytorch.org for PyTorch install instructions.)

### Installation
To work with this project on your own machine, you need to install the environmnet as follows: 

```
conda env create -f environment.yml
conda activate stylehuman
pip install nvidia-pyindex
pip install nvidia-tensorflow[horovod]
pip install nvidia-tensorboard==1.15
```
Extra notes:
1. In case having some conflicts when calling CUDA version, please try to empty the LD_LIBRARY_PATH. For example:
```
LD_LIBRARY_PATH=; python generate.py --outdir=out/stylegan_human_v2_1024 --trunc=1 --seeds=1,3,5,7 
--network=pretrained_models/stylegan_human_v2_1024.pkl --version 2
```

### Train
#### Train God-Human model using Stylegan2-ada-pytorch
```
python train.py --outdir=training_results/sg2/god_human --data=data/god_human_dataset --gpus=4 --cond=0 --aug=noaug --snap=10 --mirror=1 --cfg=shhq --square=False --workers=1 --resume=pretrained_models/stylegan_human_v2_1024.pkl
```

If you're using slurm in ICM just type:
```
sbatch run_training.sh
```

### Generate full-body images using our pretrained model
```
# Generate full-body images without truncation
python generate.py --outdir=your_outdir --trunc=1 --seeds=1,3,5,7 --network=pretrained_models/god-human-model.pkl --version 2

# Generate full-body images with truncation 
python generate.py --outdir=outputs/generate/stylegan_human_v2_1024 --trunc=0.8 --seeds=0-10 --network=pretrained_models/god-human-model.pkl --version 2
```

### Interpolation with pivotal tuning
First, download PTI weights: [e4e_w+.pt](https://drive.google.com/file/d/1NUfSJqLhsrU7c9PwAtlZ9xtrxhzS_6tu/view?usp=sharing) into `pti`.
Second, place images in 1024 x 512 resolution that you want to interpolate in `ars_electronica` directory.
Then type:
```
python interpolation_pivotal.py
```
If you're using slurm in ICM, run:
```
sbatch interpolate.sh
```

## Results
Some examples of interpolation between a real person and gods can be found [here](https://drive.google.com/drive/folders/1XGNFwB0_AW4uSKTw7xRkL2EyVm8CJZBt?usp=sharing).
