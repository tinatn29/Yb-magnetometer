import numpy as np
import csv
import sys
import ast
from ATSolver import ATSolver
import matplotlib.pyplot as plt


'''
RunMC_test_local.py 
This file is for local testing of the new code format
'''

# Set simulation parameters
delta_mod = 20  # modulation freq = 20 * gamma
theta_pol = np.pi / 2  # polarization angle
light_fields_arg = sys.argv[1]
light_fields = ast.literal_eval(light_fields_arg) # convert string argument to list of tuples
# [(Omega1, delta1), (Omega2, delta2), ...]
# detuning from m=0 level = delta * delta_mod 
# delta=2 -> 2nd harmonic sideband with detuning = 2*delta_mod from resonance

# Initialize the solver
AT = ATSolver(light_fields, delta_mod, theta_pol)

# Prepare input B-field array and velocity
# vx_input = np.load('vx_input_1000.npy') # load transverse vx from file
vx_input = np.array([0, 0.01]) # test input
# AT.b_array = np.linspace(0, 30, 31) # linear gradient in b
# AT.b_direction = 2 # b along z-axis

# Test load b fields from file
b_array_fname = "./configs/" + sys.argv[2]
AT.b_array = np.load(b_array_fname)

# calculate Doppler-averaged results
results = AT.SolveME_parallel_b_array(vx_input)
result = np.mean(results, axis=0) # average down each column

# Compute rho_e, Iy (with Hanle effect)
rho_e = result[:, 0] + result[:, 1] + result[:, 2]
Iy = result[:, 0] + 2*result[:, 1] + result[:, 2] - 2*result[:, 3]

fig, ax = plt.subplots()
plt.plot(AT.b_array[:,2], rho_e, label=r"$\rho_e$")
plt.plot(AT.b_array[:,2], Iy, label=r"$I_y$")
ax.set_xlabel(r"$b_z (\gamma)$")
ax.set_ylabel(r"Fluorescence")
ax.set_xlim([np.min(AT.b_array), np.max(AT.b_array)])
plt.legend()
plt.show()
