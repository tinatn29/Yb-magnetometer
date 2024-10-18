# Yb-magnetometer
This repository contains the code developed for the manuscript \
**“Quantum States Imaging of Magnetic Field Contours based on Autler-Townes Effect in Yb Atoms”** \
Authors: Tanaporn Na Narong, Hongquan Li, Joshua Tong, Mario Dueñas, and Leo Hollberg \
Submitted: 2024 (preprint is available [here](arxiv link)) \
\
Details of the work and code documentation are available in TN's PhD thesis \
**"Slow and fast atoms : modeling strong field effects on Yb for slowing and quantum imaging of magnetic fields"** \
Author: Tanaporn Na Narong (2023) (available online [here](https://searchworks.stanford.edu/view/in00000001635)).

## Installation
Clone the repository and make sure all the required packages are installed. We used Sherlock, a HPC cluster at Stanford University to run some of the calculations. Make sure to also upload all the files to the Sherlock/HPC directory as needed.
```
git clone https://github.com/tinatn29/Yb-magnetometer.git
cd Yb-magnetometer
```
Make sure you have Python 3.6 or higher, and the following libraries installed: 
- [Numpy](https://numpy.org/)
- [Scipy](https://scipy.org/) 
- [QuTiP: Quantum Toolbox in Python](https://qutip.org/docs/4.0.2/index.html)
- [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) 
- [matplotlib](https://matplotlib.org/)
- [pandas](https://pandas.pydata.org/)
- [jupyter notebook](https://jupyter.org/)

## Usage
The main class file `ATSolver.py` contains functions used to calculate Yb atomic fluorescence (with and without Doppler averaging) in an arbitrary magnetic field, when driven by mutiple strong, coherent light fields that are modulation sidebands of a 556 nm laser. The optical fields are driving the 1S0-3P1 transition in Yb in a 4-level V-configuration. \

To model this 4-level system, we began by deriving the time-dependent Hamiltonian matrix $H(t)$ for the four-level atom, and then used the `mesolve` function from the [QuTiP](https://qutip.org/docs/4.0.2/index.html) library to solve the [Linblad Master Equation](https://qutip.org/docs/latest/guide/dynamics/dynamics-master.html) for the density matrix $\rho$, from which we can compute the total fluorescence and the fluorescence emitted along the camera direction ($I_y$). We adapted the analysis in Jackson & Durfee (2019) to compute $I_y$.

## Documentation
Detailed documentation of the code is provided in Appendix B of [TN's thesis](https://searchworks.stanford.edu/view/in00000001635).

## Citing
If you use this code in your work, please cite the manuscript and the thesis.

