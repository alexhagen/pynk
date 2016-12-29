import numpy as np

def isotopes():
    elements = np.genfromtxt('/home/ahagen/code/pynk/isotopic_abundances.csv',
                             delimiter=' ', dtype=None)
    return elements


class compound:
    def __init__(self, formula=None, constituents=None):
        if formula is not None:
            self.process_formula(formula)
        if constituents is not None:
            self.constituents = constituents
        self.isotopes = isotopes()

        self.abundance_table = []

        self.total_atoms = np.sum([val for key,val in self.constituents.iteritems()])

        for key, val in self.constituents.iteritems():
            for isotope in self.isotopes:
                if isotope[1] == key:
                    self.abundance_table.extend([[isotope[1], isotope[0],
                                                 isotope[2] * val / self.total_atoms / 100.0]])
