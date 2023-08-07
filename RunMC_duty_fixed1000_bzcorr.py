import numpy as np
import csv
import sys
import ast
from ATSolver import ATSolver
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


'''
RunMC_duty_fixed1000.py 
This file is for Sherlock submission and takes custom arguments:
[1] <delta_mod / gamma> e.g. 20 means delta_mod = 20 * gamma
[2] <theta / deg> e.g. 90 = 90 degrees = pi/2
[3] <Omega / gamma> Rabi freq of the carrier 
[4] <duty cycle> 0.1 or 0.5 ONLY!
[5] <bx/gamma> fixed bx value
[6] <by/gamma> fixed by value
[7] <filename> e.g. "filename.csv" where the result is saved

'''

# Set simulation parameters
delta_mod = float(sys.argv[1])  # modulation freq
theta_pol = float(sys.argv[2]) * np.pi / 180  # convert polarization angle from deg to rad
Omega0 = float(sys.argv[3]) # Rabi freq of the carrier
duty = float(sys.argv[4]) # duty cycle
light_fields = []

# Set light fields
if duty == 0.1:
	Omega1, Omega2, Omega3 = Omega0 * np.array([0.107, 0.101, 0.091]) / 0.109 # Fourier amps
	light_fields = [(Omega3, -3), (Omega2, -2), (Omega1, -1), (Omega0, 0), \
					(Omega1, 1), (Omega2, 2), (Omega3, 3)]
elif duty == 0.5:
	Omega1, Omega3 = Omega0 * np.array([0.318, 0.106]) / 0.5 # Fourier amps
	light_fields = [(Omega3, -3), (Omega1, -1), (Omega0, 0), \
					(Omega1, 1), (Omega3, 3)]
else:
	print("ERROR: Duty cycle must be either 0.1 or 0.5")
	sys.exit() # exit program


# Prepare input B-field array and velocity
vx_input = np.load('./configs/vx_input_1000.npy') # load transverse vx from file

# Load b and zmm prefit
b_data = np.load("./configs/b_prefit.npy")
z_data = np.load("./configs/zmm_prefit.npy")
# bx and by from arguments
bx_fixed = float(sys.argv[5]) # take bx from argument
by_fixed = float(sys.argv[6]) # take by from argument
# calculate bz_data
bz_data = np.zeros_like(b_data)
b_data[b_data==0] = np.sqrt(bx_fixed**2 + by_fixed**2)
diff = b_data**2 - bx_fixed**2 - by_fixed**2
bz_data[diff > 0] = np.sqrt(b_data[diff > 0]**2 - bx_fixed**2 - by_fixed**2)

# Fit bz from bz_data and z_data
def func_quad(x, a, b, c):
    return a*x**2 + b*x + c
popt, pcov = curve_fit(func_quad, z_data, bz_data)

zlist = np.linspace(-15, 15, 121)
bz = func_quad(zlist, *popt)
bx = np.ones_like(bz) * bx_fixed
by = np.ones_like(bz) * by_fixed 

# Initialize the solver
AT = ATSolver(light_fields, delta_mod, theta_pol)
AT.b_array = np.array([bx, by, bz]).transpose() # prepare b_array for calculations

# calculate Doppler-averaged results
results = AT.SolveME_parallel_b_array(vx_input)
result = np.mean(results, axis=0) # Taking Doppler average (average results over all atoms' velocities present)

# Filename from argument
filename = sys.argv[7]
np.savetxt(filename, result, delimiter=',') # save result as csv 
