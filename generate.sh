#!/bin/bash -l
#SBATCH -J stylehuman_generate
#SBATCH -C volta
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=1
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --account=g92-1475
#SBATCH --time=0-01:00:00
#SBATCH --qos=normal
#SBATCH --output=output_generate.txt
#SBATCH --mem=40G

module load common/anaconda/3.8
module load common/compilers/gcc/12.2.0
module load gpu/cuda/12.0
conda activate $HOME/envs/stylehuman
python generate.py --outdir=outputs/generate/god-human-trunc-1 --trunc=1 --seeds=0-10 --network=training_results/sg2/god_human/00010-god_human_dataset-rectangle-mirror-shhq4-noaug-resumecustom/network-snapshot-000080.pkl --version 2
