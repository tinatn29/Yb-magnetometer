#!/bin/bash
#SBATCH --job-name=20_fixed1000_0.0deg_5.0_0.1duty_bx0.0_by1.0.job
#SBATCH --output=./out/20_fixed1000_0.0deg_5.0_0.1duty_bx0.0_by1.0.txt
#SBATCH --error=./err/20_fixed1000_0.0deg_5.0_0.1duty_bx0.0_by1.0.txt
#SBATCH -c 32
#SBATCH -N 1
#SBATCH --time=0-10:00
#SBATCH --mem=64000
#SBATCH --qos=normal
#SBATCH -p hns
ml python/3.6.1
python3 $SCRATCH/AT_data/RunMC_Josh_bxby_duty.py 20.0 0.0 5.0 0.1 			0.0 1.0 20_fixed1000_0.0deg_5.0_0.1duty_bx0.0_by1.0.csv