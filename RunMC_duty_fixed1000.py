import numpy as np
import csv
import sys
import ast
from ATSolver import ATSolver
import matplotlib.pyplot as plt


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

# Initialize the solver
AT = ATSolver(light_fields, delta_mod, theta_pol)

# Prepare input B-field array and velocity
vx_input = np.load('./configs/vx_input_1000.npy') # load transverse vx from file
bz_fname = "./configs/" + "bz_frames_2_new.npy"
bz = np.load(bz_fname) # load bz from file
bx_fixed = float(sys.argv[5]) # take bx from argument
bx = np.ones_like(bz) * bx_fixed
by_fixed = float(sys.argv[6]) # take by from argument
by = np.ones_like(bz) * by_fixed 
AT.b_array = np.array([bx, by, bz]).transpose() # prepare b_array for calculations


# calculate Doppler-averaged results
results = AT.SolveME_parallel_b_array(vx_input)
result = np.mean(results, axis=0) # average down each column

# Filename from argument
filename = sys.argv[7]
np.savetxt(filename, result, delimiter=',') # save result as csv 


'''
# Test load b fields from file
vx_input = np.array([0, 0.01, 0.1, 0.2]) # test input
b_array_fname = "./configs/" + "bz_frames_2_new.npy"
AT.b_array = np.load(b_array_fname)
AT.b_direction = 2 # b along z

# calculate Doppler-averaged results
results = AT.SolveME_parallel_b_array(vx_input, max_cores=4)
result = np.mean(results, axis=0) # average down each column
Iy = (result[:,0] + 2*result[:,1] + result[:,2] - 2*result[:,3]) / 2
plt.plot(AT.b_array, Iy)
plt.show()
'''

