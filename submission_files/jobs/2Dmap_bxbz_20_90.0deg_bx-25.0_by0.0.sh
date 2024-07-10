#!/bin/bash
#SBATCH --job-name=2Dmap_bxbz_20_90.0deg_bx-25.0_by0.0.job
#SBATCH --output=./out/2Dmap_bxbz_20_90.0deg_bx-25.0_by0.0.txt
#SBATCH --error=./err/2Dmap_bxbz_20_90.0deg_bx-25.0_by0.0.txt
#SBATCH -c 32
#SBATCH -N 1
#SBATCH --time=0-03:00
#SBATCH --mem=64000
#SBATCH --qos=normal
#SBATCH -p hns
ml python/3.6.1
python3 $SCRATCH/AT_data/RunMC_configs_N_bxby.py 20.0 90.0 "[(10,-1),(10,0),(10,1)]" bz_2Dmap_25.npy -25.0 0 500 2Dmap_bxbz_20_90.0deg_bx-25.0_by0.0.csv