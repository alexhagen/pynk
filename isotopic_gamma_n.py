from pynk.talys import talys as t
from pym import func as f
import numpy as np

elements = np.genfromtxt('/home/ahagen/code/pynk/isotopic_abundances.csv',
                         delimiter=' ', dtype=None)
#elements = [(9, 'Be', 100.)]
for element in elements[:10]:
    if element[1] != 'H' and element[1] != 'He':
        input = t(Z=element[1], A=element[0],
                  energy=np.logspace(-8., np.log10(20.), 20),
                  projectile='g', ejectile='n')
        input.run()
        input.proc_output()
        curve = f.curve(input.E, input.sigma,
                        name=r'$\sigma_{\left(\gamma, n\right)}$')
        if np.max(input.sigma > 0.0):
            print '%s-%d: Q = %f' % (element[1], element[0], input.Q)
