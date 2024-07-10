#!/bin/bash
#SBATCH --job-name=1mW_11_2.6_fixed1000_90deg_0.1duty_newbz.job
#SBATCH --output=./out/1mW_11_2.6_fixed1000_90deg_0.1duty_newbz.txt
#SBATCH --error=./err/1mW_11_2.6_fixed1000_90deg_0.1duty_newbz.txt
#SBATCH -c 32
#SBATCH -N 1
#SBATCH --time=0-12:00
#SBATCH --mem=64000
#SBATCH --qos=normal
#SBATCH -p hns
ml python/3.6.1
python3 $SCRATCH/AT_data/RunMC_duty_powerdep.py 11.0 90.0 2.6009 0.1 0 0 1mW_11_2.6_fixed1000_90deg_0.1duty_newbz.csv