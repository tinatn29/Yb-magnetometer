# Yb-magnetometer [DRAFT]
This repository contains the code developed for the manuscript \
“Quantum States Imaging of Magnetic Field Contours based on Autler-Townes Effect in Yb Atoms”



the work published in Na Narong, et al. (preprint) [[1]](arxiv link) and TN's PhD thesis (2023)[[2]](https://searchworks.stanford.edu/view/in00000001635).
Numerical model to calculate Yb atomic fluorescence 

## Numerical calculation of Yb atomic fluorescence
We derived the time-dependent Hamiltonian matrix $H(t)$ for the four-level atom, and then used the `mesolve` function from the [QuTiP](https://qutip.org/docs/4.0.2/index.html) library to solve the [Linblad Master Equation](https://qutip.org/docs/latest/guide/dynamics/dynamics-master.html) for density matrix. 

From the density matrix, we extract the total excited-state population $\rho_e$ (total fluorescence is directly proportional to $\rho_e$).
We also compute the fluorescence emitted vertically ($I_y$). The derivation presented in [2] is based on the supplemental material of Jackson & Durfee (2019)[3].

## Documentation
Detailed documentation of the code is provided in Appendix B of TN's thesis [2].

## Software and Libraries
- Python 3.6
- [Numpy](https://numpy.org/)
- [QuTiP: Quantum Toolbox in Python](https://qutip.org/docs/4.0.2/index.html)
- [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) 
- [matplotlib](https://matplotlib.org/)
- [pandas](https://pandas.pydata.org/)
- [jupyter notebook](https://jupyter.org/)
  
## References
1. Paper / arxiv
2. Na Narong, Tanaporn (thesis)
3. Jackson & Durfee paper
