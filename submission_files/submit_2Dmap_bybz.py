#!/usr/bin/env python

import os
import sys
import ast
import numpy as np


# single job submission (1000 atoms)
delta_mod = float(sys.argv[1]) # [1] <delta_mod / gamma> e.g. 20 means delta_mod = 20 * gamma
theta = float(sys.argv[2]) # [2] polarization angle
light_fields = sys.argv[3] # [3] light fields as strings e.g. "[(10,-1),(10,1)]"
light_fields_list = ast.literal_eval(light_fields) # list format of light_fields

b_array_fname = 'bz_2Dmap_25.npy' # filename for bz array

# custom fixed bx by values
by_array = np.linspace(-25, 25, 51) # by for each slice in the 2D map
bx = float(sys.argv[4]) # take bx from argument
N = 500

for i in range(len(by_array)):
	by = by_array[i]
	job_file = os.path.join(os.getcwd(),f"./jobs/2Dmap_bxbz_{delta_mod:.0f}_{theta:.1f}deg_bx{bx:.1f}_by{by:.1f}.sh")

	with open(job_file, 'w') as fh:
		fh.writelines("#!/bin/bash\n")
		fh.writelines(f"#SBATCH --job-name=2Dmap_bxbz_{delta_mod:.0f}_{theta:.1f}deg_bx{bx:.1f}_by{by:.1f}.job\n")
		fh.writelines(f"#SBATCH --output=./out/2Dmap_bxbz_{delta_mod:.0f}_{theta:.1f}deg_bx{bx:.1f}_by{by:.1f}.txt\n")
		fh.writelines(f"#SBATCH --error=./err/2Dmap_bxbz_{delta_mod:.0f}_{theta:.1f}deg_bx{bx:.1f}_by{by:.1f}.txt\n")
		fh.writelines("#SBATCH -c 32\n")
		fh.writelines("#SBATCH -N 1\n")
		fh.writelines("#SBATCH --time=0-03:00\n")
		fh.writelines("#SBATCH --mem=64000\n")
		fh.writelines("#SBATCH --qos=normal\n")
		fh.writelines("#SBATCH -p hns\n")
		fh.writelines("ml python/3.6.1\n")
		fh.writelines([f"python3 $SCRATCH/AT_data/RunMC_configs_N_bxby.py {delta_mod} {theta} ", '"', light_fields, '" ',\
			b_array_fname, ' ',
			f" {bx} {by} {N} 2Dmap_bxbz_{delta_mod:.0f}_{theta:.1f}deg_bx{bx:.1f}_by{by:.1f}.csv"])

	os.system("sbatch %s" %job_file)