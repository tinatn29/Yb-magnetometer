import numpy as np
import csv
import sys
import ast
from ATSolver import ATSolver


'''
RunMC_bxby_fixed1000.py 
This file is for Sherlock submission and takes fixed bx, by values (with weak bz gradient):
[1] <delta_mod / gamma> e.g. 20 means delta_mod = 20 * gamma
[2] <theta / deg> e.g. 90 = 90 degrees = pi/2
[3] <light_fields> as strings e.g. "[(10,-1),(10,1)]" would create 2 sidebands with 
Omega1=Omega2=10 and detunings = -1*delta_mod and 1*delta_mod from m=0 state
[4] <bx/gamma> fixed bx value
[5] <by/gamma> fixed by value
[6] <filename> e.g. "filename.csv" where the result is saved

'''

# Set simulation parameters
delta_mod = float(sys.argv[1])  # modulation freq
theta_pol = float(sys.argv[2]) * np.pi / 180  # convert polarization angle from deg to rad
light_fields_arg = sys.argv[3]
light_fields = ast.literal_eval(light_fields_arg) # convert string argument to list of tuples
# [(Omega1, delta1), (Omega2, delta2), ...]
# detuning from m=0 level = delta * delta_mod 
# delta=2 -> 2nd harmonic sideband with detuning = 2*delta_mod from resonance

# Initialize the solver
AT = ATSolver(light_fields, delta_mod, theta_pol)

# Prepare input B-field array and velocity
vx_input = np.load('./configs/vx_input_500.npy') # load transverse vx from file

bz = np.linspace(-15, 15, 121)
bx_fixed = float(sys.argv[4]) # take bx from argument
bx = np.ones_like(bz) * bx_fixed
by_fixed = float(sys.argv[5]) # take by from argument
by = np.ones_like(bz) * by_fixed 
AT.b_array = np.array([bx, by, bz]).transpose()

# calculate Doppler-averaged results
results = AT.SolveME_parallel_b_array(vx_input)
result = np.mean(results, axis=0) # average down each column

# Filename from argument
filename = sys.argv[6]
np.savetxt(filename, result, delimiter=',') # save result as csv 
