#!/bin/bash
#SBATCH --job-name=1mW_20_2.6_fixed1000_90deg_0.1duty_HqFrames.job
#SBATCH --output=./out/1mW_20_2.6_fixed1000_90deg_0.1duty_HqFrames.txt
#SBATCH --error=./err/1mW_20_2.6_fixed1000_90deg_0.1duty_HqFrames.txt
#SBATCH -c 32
#SBATCH -N 1
#SBATCH --time=0-8:00
#SBATCH --mem=64000
#SBATCH --qos=normal
#SBATCH -p hns
ml python/3.6.1
python3 $SCRATCH/AT_data/RunMC_duty_fixed1000.py 20.0 90.0 2.600944137591695 0.1 1mW_20_2.6_fixed1000_90deg_0.1duty_HqFrames.csv