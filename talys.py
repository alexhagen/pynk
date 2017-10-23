import subprocess
import notify2 as n
import re
import os
from os.path import expanduser

class talys:
    r""" A Talys object develops a TALYS simulation for theoretical
        cross section simulation.
        
        :param int A: the mass number of the target
        :param int Z: the atomic number of the target
        :param str projectile: the abbreviation of the projectile particle
        :param str ejectile: if specified, only outputs results for given
            ejectiles
        :param list energy: a list of energies to evaluate at
        :param list level: a list of energy levels to evaluate at
    """
    fullnames = {'n': 'neutron', 'g': 'gamma'}
    def __init__(self, A=None, Z=None, projectile='n', ejectile=None,
                 energy=None, level=None):
        if A is None:
            pass
        else:
            self.A = A
        if Z is None:
            pass
        else:
            self.Z = Z
        if projectile is None:
            pass
        else:
            self.projectile = projectile
        if ejectile is None:
            pass
        else:
            self.ejectile = ejectile
        if energy is None:
            pass
        else:
            self.energy = energy
        if level is None:
            pass
        else:
            self.level = level

        self.filename = '%s-%d_%s-%s.inp' % \
            (self.Z, self.A, self.projectile, self.ejectile)
        with open(self.filename, 'w') as f:
            f.write('element %s\n' % (self.Z.lower()))
            f.write('mass %d\n' % (self.A))
            f.write('projectile %s\n' % (self.projectile.lower()))
            f.write('ejectiles %s\n' % (self.ejectile.lower()))
            if level is not None:
                f.write('Ltarget %d\n' % (self.level))
            if len(energy) > 1:
                self.energyfilename = '%s-%d_%s-%s_energies.inp' % \
                    (self.Z, self.A, self.projectile, self.ejectile)
                f.write('energy %s\n' % (self.energyfilename))
                with open(self.energyfilename, 'w') as f2:
                    for e in energy:
                        f2.write('%.15f\n' % (e))
    def run(self, datadir=None):
        if datadir is None:
            datadir = 'archive/'
        self.out_filename = '%s-%d_%s-%s.out' % \
            (self.Z, self.A, self.projectile, self.ejectile)
        if os.path.isfile(datadir + self.out_filename):
            self.out_filename = datadir + self.out_filename
        else:
            cmd = 'talys < %s > %s' % (self.filename, self.out_filename)
            os.system(cmd)
        return self

    def proc_output(self, addtl_rxns=[]):
        self.E = []
        self.sigma = []
        self.nu = []
        self.rxns = {}
        lines = open(self.out_filename, 'r').readlines()
        for line in lines:
            if 'Q(g,n):' in line:
                arr = re.findall(r"[\-+]?\d*\.\d+|[\-+]?\d+", line)
                self.Q = float(arr[0])
            if '########### REACTION SUMMARY FOR E=' in line:
                arr = re.findall(r"[\-+]?\d*\.\d+|[\-+]?\d+", line)
                if len(arr) > 1:
                    E = float(arr[0]) * 10.**float(arr[1])
                else:
                    E = float(arr[0])
                self.E.extend([E])
            if self.fullnames[self.ejectile] in line \
                and 'Multiplicity' in line:
                arr = re.findall(r"[\-+]?\d*\.\d+|[\-+]?\d+", line)
                sigma = float(arr[0]) * 10.**float(arr[1])
                nu = float(arr[2]) * 10.**float(arr[3])
                self.sigma.extend([sigma])
                self.nu.extend([nu])
            for rxn in addtl_rxns:
                if rxn in line and self.mult_in_line:
                    arr = re.findall(r"[\-+]?\d*\.\d+|[\-+]?\d+", line)
                    sigma = float(arr[0]) * 10.**float(arr[1])
                    if rxn not in self.rxns:
                        self.rxns[rxn] = [[],[]]
                    self.rxns[rxn][0].extend([E])
                    self.rxns[rxn][1].extend([sigma])
            if 'Multiplicity' in line:
                self.mult_in_line = True
            else:
                self.mult_in_line = False
        return self

    def clean(self):
        os.system('rm -f %s %s *.tot' % (self.filename, self.energyfilename))
        os.system('mkdir -p archive')
        if 'archive' not in self.out_filename:
            os.system('mv %s archive/' % (self.out_filename))
