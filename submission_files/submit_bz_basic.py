#!/usr/bin/env python

import os
import sys
import ast
import numpy as np


# single job submission (1000 atoms)
delta_mod = float(sys.argv[1]) # [1] <delta_mod / gamma> e.g. 20 means delta_mod = 20 * gamma
theta = float(sys.argv[2]) # [2] <theta / pi> e.g. 90 means 90 degrees
light_fields = sys.argv[3] # [3] light fields as strings e.g. "[(10,-1),(10,1)]"
b_array_fname = "bz_twosides_60.npy" # basic bz linear gradient from 0 to 75

light_fields_list = ast.literal_eval(light_fields) # list format of light_fields
num_freqs = len(light_fields_list)

job_file = os.path.join(os.getcwd(),f"./jobs/{delta_mod:.0f}_fixed1000_{theta:.0f}deg_{num_freqs}bands_bz60.sh")

with open(job_file, 'w') as fh:
	fh.writelines("#!/bin/bash\n")
	fh.writelines(f"#SBATCH --job-name={delta_mod:.0f}_fixed1000_{theta:.0f}deg_{num_freqs}bands_bz60.job\n")
	fh.writelines(f"#SBATCH --output=./out/{delta_mod:.0f}_fixed1000_{theta:.0f}deg_{num_freqs}bands_bz60.txt\n")
	fh.writelines(f"#SBATCH --error=./err/{delta_mod:.0f}_fixed1000_{theta:.0f}deg_{num_freqs}bands_bz60.txt\n")
	fh.writelines("#SBATCH -c 32\n")
	fh.writelines("#SBATCH -N 1\n")
	fh.writelines("#SBATCH --time=0-8:00\n")
	fh.writelines("#SBATCH --mem=64000\n")
	fh.writelines("#SBATCH --qos=normal\n")
	fh.writelines("#SBATCH -p hns\n")
	fh.writelines("ml python/3.6.1\n")
	fh.writelines([f"python3 $SCRATCH/AT_data/RunMC_configs_fixed1000.py {delta_mod} {theta} ", '"', light_fields, '" ',\
		b_array_fname, 
		f" {delta_mod:.0f}_fixed1000_{theta:.0f}deg_{num_freqs}bands_bz60.csv"])

os.system("sbatch %s" %job_file)