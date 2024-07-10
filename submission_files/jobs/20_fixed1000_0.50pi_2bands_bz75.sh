#!/bin/bash
#SBATCH --job-name=20_fixed1000_0.50pi_2bands_bz75.job
#SBATCH --output=./out/20_fixed1000_0.50pi_2bands_bz75.txt
#SBATCH --error=./err/20_fixed1000_0.50pi_2bands_bz75.txt
#SBATCH -c 32
#SBATCH -N 1
#SBATCH --time=0-6:00
#SBATCH --mem=64000
#SBATCH --qos=normal
#SBATCH -p hns
ml python/3.6.1
python3 $SCRATCH/AT_data/RunMC_configs_fixed1000.py 20.0 0.5 "[(10,-1),(10,1)]" bz_linear_75.npy 20_fixed1000_0.50pi_2bands_bz75.csv