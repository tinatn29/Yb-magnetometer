import numpy as np
from qutip import *
from scipy import signal
import time
import copy


'''
======== Hamiltonian for mesolve (time-dependent solver) ========
H0 contains the time-independent diagonal elements
H0 is a function of (bx, by, bz)
'''
def H0_4fields(args):
	# Time-independent elements of the Hamiltonian [magnetic-field dependent]
	b_cross_term = (args['b'][0] + 1j * args['b'][1]) / np.sqrt(2)
	H0 = Qobj([[0, 0, 0, 0], \
		[0, args['b'][2], np.conj(b_cross_term) , 0], \
        [0, b_cross_term, 0, np.conj(b_cross_term)], \
        [0, 0, b_cross_term, -args['b'][2]]])
	return H0


# time-dependent coefficient for sigma+ sigma- terms 
def coeff_sigma_terms(t, args):
	a = args['Omegas'] * args['gamma'] * np.exp(1j * t * \
		(args['Deltas'] * args['delta_mod'] * args['gamma'] - args['k'] * args['vx']))
	return -1j * a.sum() * np.sin(args['theta_pol']) / (2 * np.sqrt(6))

# time-dependent coefficient for sigma+ sigma- terms (complex conj)
def coeff_sigma_terms_conj(t, args):
	return np.conj(coeff_sigma_terms(t, args))

# time-dependent coefficient for pi terms
def coeff_pi_terms(t, args):
	a = args['Omegas'] * args['gamma'] * np.exp(1j * t * \
		(args['Deltas'] * args['delta_mod'] * args['gamma'] - args['k'] * args['vx']))
	return a.sum() * np.cos(args['theta_pol']) / (2 * np.sqrt(3))

# time-dependent coefficient for pi terms (complex conj)
def coeff_pi_terms_conj(t, args):
	return np.conj(coeff_pi_terms(t, args))


# Define class here
class ATSolver():
	def __init__(self, light_fields=[], delta_mod=20, theta_pol=np.pi/2):
		Omegas, Deltas = zip(*light_fields)
		self.args = {
					'gamma': 2 * np.pi * 182e3, # natural linewidth
					'theta_pol': theta_pol, # polarization angle (0: horizontal (z), pi/2: vertical (y))
					'Omegas': np.array(Omegas), # list of Rabi frequencies (units of gamma)
					'Deltas': np.array(Deltas), # list of detunings (units of delta_mod)
					'delta_mod': delta_mod, # laser modulation frequency (units of gamma)
					'k': 2 * np.pi / 556e-9, # wavenumber
					'vx': 0, # atom's velocity
					'b': np.array([0.0, 0.0, 0.0]) # g * mu * B (magnetic field in units of gamma)
		}

		# Hamiltonian H1 and H2 for time-dependent solver
		self.H_cos = Qobj([[0, 1, 0, 1], \
			[0, 0, 0, 0], \
			[0, 0, 0, 0], \
			[0, 0, 0, 0]])
		self.H_cos_dag = self.H_cos.dag()

		self.H_sin = Qobj([[0, 0, 1, 0], \
			[0, 0, 0, 0], \
			[0, 0, 0, 0], \
			[0, 0, 0, 0]])
		self.H_sin_dag = self.H_sin.dag()

		self.tlist = np.linspace(0, 20, 100) / self.args['gamma']
		self.psi0 = fock_dm(4, 0)  # start in ground state

		# Collapse operators (3 decays)
		g = basis(4, 0) # ground state
		ep = basis(4, 1) # m = 1
		e0 = basis(4, 2) # m = 0
		em = basis(4, 3) # m = -1
		self.c_op_list = [np.sqrt(self.args['gamma']) * g * ep.dag(), \
			np.sqrt(self.args['gamma']) * g * e0.dag(), \
			np.sqrt(self.args['gamma']) * g * em.dag()]

		# B-field properties (set this manually if running for an array of b values)
		self.b_array = None
		# b_array can be a 1D array e.g. np.linspace(0, 60, 61) OR
		# a 2D array e.g. [[0,0,0], [0,0,1], [0,0,2], ...]
		self.b_direction = 2 # int 0,1,2 corresponding to bx,by,bz

		# output density matrix elements
		self.rho11 = 0.0 # population of m=1 state
		self.rho22 = 0.0 # population of m=0 state
		self.rho33 = 0.0 # population of m=-1 state
		self.rho13_Re = 0.0 # coherence between m=1 and m=-1 (real part only)


	'''
	======== Time-dependent solver (4 fields) with Doppler ========
	'''
	def SolveME_single(self):
		# Solve for steady-state rho11, rho22, rho33, rho13 for a single atom 
		# Single velocity, single b-field value
		H0 = H0_4fields(self.args)
		H = [H0, [self.H_cos, coeff_sigma_terms], [self.H_cos_dag, coeff_sigma_terms_conj], \
		[self.H_sin, coeff_pi_terms], [self.H_sin_dag, coeff_pi_terms_conj]]

		output = mesolve(H, self.psi0, self.tlist, c_ops=self.c_op_list, args=self.args)
		# Extract steady-state rhos
		N = len(self.tlist[self.tlist * self.args['gamma'] > 10])
		# Reset to make sure
		self.rho11 = 0
		self.rho22 = 0
		self.rho33 = 0
		self.rho13_Re = 0

		for i in range(N):
			rho = output.states[i+N]
			self.rho11 += rho[1,1]
			self.rho22 += rho[2,2]
			self.rho33 += rho[3,3]
			self.rho13_Re += rho[1,3]
    	
    	# calculate mean
		self.rho11 = np.real(self.rho11 / N)
		self.rho22 = np.real(self.rho22 / N)
		self.rho33 = np.real(self.rho33 / N)
		self.rho13_Re = np.real(self.rho13_Re / N)

	'''
	======== Solve for rhos for a 1D b-array ========
	'''
	def SolveME_single_b_array(self, vx):
		# This function calculates the density matrix (steady-state) for a range (array) of B-field values
		# make sure self.b_array and self.b_direction are set for this function to work properly
		self.args['vx'] = vx # set atom's velocity
		N = len(self.b_array)
		dim = len(np.shape(self.b_array)) # dimensions of b_array (1 or 2)

		# result array [rho11, rho22, rho33, Re(rho13)] each row (each value of b_array)
		result = np.zeros((len(self.b_array), 4)) # 2D output dim(len(b_array), 4)

		# Iterate through all values in b_array
		for i in range(len(self.b_array)):
			# Set magnetic field
			if dim == 1:
				self.args['b'][self.b_direction] = self.b_array[i] * self.args['gamma']
			elif dim == 2 and np.shape(self.b_array)[1] == 3:
				self.args['b'] = self.b_array[i] * self.args['gamma']
			else:
				print("ERROR: b_array must be a 1D array or a 2D array with 3 columns")
				return

			# Solve for rho
			self.SolveME_single()
			result[i, 0] = self.rho11
			result[i, 1] = self.rho22
			result[i, 2] = self.rho33
			result[i, 3] = self.rho13_Re

		return result # return 2D output array [rho11, rho22, rho33, Re(rho13)]


	def SolveME_parallel_b_array(self, vx_input, max_cores=32):
		# Calculate Doppler averaged rho from lots of atoms using parallel computing
		# vx_input corresponds to atoms' velocities we are using
		import multiprocessing as mp
		start_time = time.time()
		n_cores = np.amin([mp.cpu_count(), max_cores])
		# Use no. of CPUs available (locally) or 32 cores maximum (Sherlock cluster)
		pool = mp.Pool(processes=n_cores)

		results = pool.map(self.SolveME_single_b_array, vx_input)
		print('Time elapsed: {0:.2f} sec'.format(time.time() - start_time))

		return results

