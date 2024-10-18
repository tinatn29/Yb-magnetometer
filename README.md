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
To run the code, first clone the repository and install the required dependencies:
```
git clone https://github.com/tinatn29/Yb-magnetometer.git
cd Yb-magnetometer
```
Make sure you have Python 3.6 or higher, and the following libraries installed: 
- [Numpy](https://numpy.org/)
- [QuTiP: Quantum Toolbox in Python](https://qutip.org/docs/4.0.2/index.html)
- [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) 
- [matplotlib](https://matplotlib.org/)
- [pandas](https://pandas.pydata.org/)
- [jupyter notebook](https://jupyter.org/)

## Usage
We derived the time-dependent Hamiltonian matrix $H(t)$ for the four-level atom, and then used the `mesolve` function from the [QuTiP](https://qutip.org/docs/4.0.2/index.html) library to solve the [Linblad Master Equation](https://qutip.org/docs/latest/guide/dynamics/dynamics-master.html) for density matrix. 

From the density matrix, we extract the total excited-state population $\rho_e$ (total fluorescence is directly proportional to $\rho_e$).
We also compute the fluorescence emitted vertically ($I_y$). The derivation presented in [2] is based on the supplemental material of Jackson & Durfee (2019)[3].

## Documentation
Detailed documentation of the code is provided in Appendix B of TN's thesis [2].

## Citing
If you use this code in your work, please cite the manuscript and the thesis.

