#!/bin/bash -l
#SBATCH -J stylehuman_interpolation
#SBATCH -C volta
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=1
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --account=g92-1475
#SBATCH --time=0-00:30:00
#SBATCH --qos=normal
#SBATCH --output=output_inference.txt
#SBATCH --mem=40G

module load common/anaconda/3.8
module load common/compilers/gcc/12.2.0
module load gpu/cuda/12.0

rm -r outputs/pti/embeddings/test/PTI/*
rm -r outputs/videos/*
python draw_gods.py 10
cp ./prepare_room/* ./ars_electronica

conda activate $HOME/envs/stylehuman
#python prepare_photo.py prepare_room
python interpolation_pivotal.py

rm ./ars_electronica/*
