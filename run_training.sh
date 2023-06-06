#!/bin/bash -l
#SBATCH -J stylehuman_training
#SBATCH -C volta
#SBATCH --gres=gpu:4
#SBATCH --cpus-per-task=1
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --account=g92-1475
#SBATCH --time=2-00:00:00
#SBATCH --qos=normal
#SBATCH --output=output.txt
#SBATCH --mem=40G

module load common/anaconda/3.8
module load common/compilers/gcc/12.2.0
module load gpu/cuda/12.1
conda activate $HOME/envs/stylehuman
python train.py --outdir=training_results/sg2/god_human --data=data/god_human_dataset --gpus=4 --cond=0 --aug=noaug --snap=10 --mirror=1 --cfg=shhq --square=False --workers=1 --resume=pretrained_models/stylegan_human_v2_1024.pkl
