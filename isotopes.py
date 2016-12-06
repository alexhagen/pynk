import numpy as np

def isotopes():
    elements = np.genfromtxt('/home/ahagen/code/pynk/isotopic_abundances.csv',
                             delimiter=' ', dtype=None)
    return elements
