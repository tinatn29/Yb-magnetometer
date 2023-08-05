#!/usr/bin/env python

import os
import sys
import ast
import numpy as np


# single job submission (1000 atoms)
delta_mod = float(sys.argv[1]) # [1] <delta_mod / gamma> e.g. 20 means delta_mod = 20 * gamma
theta = float(sys.argv[2]) # [2] <theta / pi> e.g. 90 means 90 degrees
Omega0 = float(sys.argv[3]) # [3] Rabi freq of carrier
duty = float(sys.argv[4]) # [4] duty cycle 0.1 or 0.5

# custom fixed bx by values
bx = float(sys.argv[5])
by = float(sys.argv[6])

job_file = os.path.join(os.getcwd(),f"./jobs/{delta_mod:.0f}_{Omega0:.1f}_fixed1000_{theta:.0f}deg_{duty}duty_HqFrames_bx{bx:.1f}_by{by:.1f}.sh")

with open(job_file, 'w') as fh:
	fh.writelines("#!/bin/bash\n")
	fh.writelines(f"#SBATCH --job-name={delta_mod:.0f}_{Omega0:.1f}_fixed1000_{theta:.0f}deg_{duty}duty_HqFrames_bx{bx:.1f}_by{by:.1f}.job\n")
	fh.writelines(f"#SBATCH --output=./out/{delta_mod:.0f}_{Omega0:.1f}_fixed1000_{theta:.0f}deg_{duty}duty_HqFrames_bx{bx:.1f}_by{by:.1f}.txt\n")
	fh.writelines(f"#SBATCH --error=./err/{delta_mod:.0f}_{Omega0:.1f}_fixed1000_{theta:.0f}deg_{duty}duty_HqFrames_bx{bx:.1f}_by{by:.1f}.txt\n")
	fh.writelines("#SBATCH -c 32\n")
	fh.writelines("#SBATCH -N 1\n")
	fh.writelines("#SBATCH --time=0-16:00\n")
	fh.writelines("#SBATCH --mem=64000\n")
	fh.writelines("#SBATCH --qos=normal\n")
	fh.writelines("#SBATCH -p hns\n")
	fh.writelines("ml python/3.6.1\n")
	fh.writelines([f"python3 $SCRATCH/AT_data/RunMC_duty_fixed1000.py {delta_mod} {theta} {Omega0} {duty} ",\
		f"{bx} {by} {delta_mod:.0f}_{Omega0:.1f}_fixed1000_{theta:.0f}deg_{duty}duty_HqFrames_bx{bx:.1f}_by{by:.1f}.csv"])

os.system("sbatch %s" %job_file)