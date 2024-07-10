#!/bin/bash
#SBATCH --job-name=22_10.0_fixed1000_90deg_0.1duty_HqFrames_bx1.0_by1.0.job
#SBATCH --output=./out/22_10.0_fixed1000_90deg_0.1duty_HqFrames_bx1.0_by1.0.txt
#SBATCH --error=./err/22_10.0_fixed1000_90deg_0.1duty_HqFrames_bx1.0_by1.0.txt
#SBATCH -c 32
#SBATCH -N 1
#SBATCH --time=0-10:00
#SBATCH --mem=64000
#SBATCH --qos=normal
#SBATCH -p hns
ml python/3.6.1
python3 $SCRATCH/AT_data/RunMC_duty_fixed1000.py 22.0 90.0 10.0 0.1 1.0 1.0 22_10.0_fixed1000_90deg_0.1duty_HqFrames_bx1.0_by1.0.csv