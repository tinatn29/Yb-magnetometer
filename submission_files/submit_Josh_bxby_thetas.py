#!/usr/bin/env python

import os
import sys
import ast
import numpy as np


# single job submission (1000 atoms)
delta_mod = float(sys.argv[1]) # [1] <delta_mod / gamma> e.g. 20 means delta_mod = 20 * gamma
light_fields = sys.argv[2] # [2] light fields as strings e.g. "[(10,-1),(10,1)]"
light_fields_list = ast.literal_eval(light_fields) # list format of light_fields
num_freqs = len(light_fields_list)

# custom fixed bx by values
bx = float(sys.argv[3])
by = float(sys.argv[4])

thetas = np.array([0.0, 11.2, 22.5, 33.8, 45.0, 56.2, 67.5, 78.8, 90.0]) 
# polarization angles from Josh's data

for theta in thetas:
	job_file = os.path.join(os.getcwd(),f"./jobs/{delta_mod:.0f}_fixed1000_{theta:.1f}deg_{num_freqs}bands_bx{bx:.1f}_by{by:.1f}.sh")

	with open(job_file, 'w') as fh:
		fh.writelines("#!/bin/bash\n")
		fh.writelines(f"#SBATCH --job-name={delta_mod:.0f}_fixed1000_{theta:.1f}deg_{num_freqs}bands_bx{bx:.1f}_by{by:.1f}.job\n")
		fh.writelines(f"#SBATCH --output=./out/{delta_mod:.0f}_fixed1000_{theta:.1f}deg_{num_freqs}bands_bx{bx:.1f}_by{by:.1f}.txt\n")
		fh.writelines(f"#SBATCH --error=./err/{delta_mod:.0f}_fixed1000_{theta:.1f}deg_{num_freqs}bands_bx{bx:.1f}_by{by:.1f}.txt\n")
		fh.writelines("#SBATCH -c 32\n")
		fh.writelines("#SBATCH -N 1\n")
		fh.writelines("#SBATCH --time=0-10:00\n")
		fh.writelines("#SBATCH --mem=64000\n")
		fh.writelines("#SBATCH --qos=normal\n")
		fh.writelines("#SBATCH -p hns\n")
		fh.writelines("ml python/3.6.1\n")
		fh.writelines([f"python3 $SCRATCH/AT_data/RunMC_Josh_bxby_fixed1000.py {delta_mod} {theta} ", '"', light_fields, '" ',\
			f"{bx} {by} {delta_mod:.0f}_fixed1000_{theta:.1f}deg_{num_freqs}bands_bx{bx:.1f}_by{by:.1f}.csv"])

	os.system("sbatch %s" %job_file)