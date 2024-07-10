#!/usr/bin/env python

import os
import sys
import numpy as np

# submit jobs for power dependence plot (duty = 0.1)
# peak power = power measured / 0.1
duty = 0.1 # duty cycle
power = np.linspace(1, 17, 17)
peak_power = power / duty
# compute Omega0 (carrier)
alphas = np.array([0.091, 0.101, 0.107, 0.109, 0.107, 0.101, 0.091]) # Fourier amplitudes
sumsq_alphas = np.sum(alphas**2)
area = 0.3 * 3 # area in cm^2
Isat = 0.136 # mW/cm^2

# array of Omega0 (Rabi freq of carrier)
Omegas = 0.109 * np.sqrt(peak_power / (2 * sumsq_alphas * area * Isat))

delta_mod = float(sys.argv[1]) # delta_mod, from data use 11 = 2 MHz
theta = float(sys.argv[2]) # 90 degrees by default
bx = float(sys.argv[3]) # bx from argument
by = float(sys.argv[4]) # by from argument

for i in range(len(Omegas)):
	Omega0 = Omegas[i] # Rabi freq of carrier
	p = power[i] # measured power in mW

	job_file = os.path.join(os.getcwd(),f"./jobs/{p:.0f}mW_{delta_mod:.0f}_{Omega0:.1f}_fixed1000_{theta:.0f}deg_{duty}duty_newbz_bx{bx}_by{by}.sh")

	with open(job_file, 'w') as fh:
		fh.writelines("#!/bin/bash\n")
		fh.writelines(f"#SBATCH --job-name={p:.0f}mW_{delta_mod:.0f}_{Omega0:.1f}_fixed1000_{theta:.0f}deg_{duty}duty_newbz_bx{bx}_by{by}.job\n")
		fh.writelines(f"#SBATCH --output=./out/{p:.0f}mW_{delta_mod:.0f}_{Omega0:.1f}_fixed1000_{theta:.0f}deg_{duty}duty_newbz_bx{bx}_by{by}.txt\n")
		fh.writelines(f"#SBATCH --error=./err/{p:.0f}mW_{delta_mod:.0f}_{Omega0:.1f}_fixed1000_{theta:.0f}deg_{duty}duty_newbz_bx{bx}_by{by}.txt\n")
		fh.writelines("#SBATCH -c 32\n")
		fh.writelines("#SBATCH -N 1\n")
		fh.writelines("#SBATCH --time=0-12:00\n")
		fh.writelines("#SBATCH --mem=64000\n")
		fh.writelines("#SBATCH --qos=normal\n")
		fh.writelines("#SBATCH -p hns\n")
		fh.writelines("ml python/3.6.1\n")
		fh.writelines([f"python3 $SCRATCH/AT_data/RunMC_duty_powerdep.py {delta_mod} {theta} {Omega0:.4f} {duty} ",\
			f"{bx} {by} {p:.0f}mW_{delta_mod:.0f}_{Omega0:.1f}_fixed1000_{theta:.0f}deg_{duty}duty_newbz_bx{bx}_by{by}.csv"])

	os.system("sbatch %s" %job_file)

