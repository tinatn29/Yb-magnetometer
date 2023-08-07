import numpy as np
import csv
import sys
import ast
from ATSolver import ATSolver


'''
RunMC_configs_fixed1000.py 
This file is for Sherlock submission and takes custom arguments:
[1] <delta_mod / gamma> e.g. 20 means delta_mod = 20 * gamma
[2] <theta / deg> e.g. 90 = 90 degrees = pi/2
[3] <light_fields> as strings e.g. "[(10,-1),(10,1)]" would create 2 sidebands with 
Omega1=Omega2=10 and detunings = -1*delta_mod and 1*delta_mod from m=0 state
[4] <b-field config> e.g. "bz.npy" to indicate the b-field input
[5] <filename> e.g. "filename.csv" where the result is saved

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
vx_input = np.load('./configs/vx_input_1000.npy') # load transverse vx from file
b_array_fname = "./configs/" + sys.argv[4]

# calculate Doppler-averaged results
results = AT.SolveME_parallel_b_array(vx_input)
result = np.mean(results, axis=0) # Taking Doppler average (average results over all atoms' velocities present)

# Filename from argument
filename = sys.argv[5]
np.savetxt(filename, result, delimiter=',') # save result as csv 
