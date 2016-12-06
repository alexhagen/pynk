from pynk.talys import talys as t
from pym import func as f
import numpy as np
import copy
from pyg.colors import pu as puc

E_g, phi_g = np.loadtxt("/home/ahagen/data/clinac_6ex_data/spectrum_bremsstrahlung.txt",
                   delimiter=',', skiprows=1, unpack=True)

spectrum = f.curve(E_g, phi_g, name='bremsstrahlung')
spectrum.normalize()
print spectrum.integrate()

elements = np.genfromtxt('/home/ahagen/code/pynk/isotopic_abundances.csv',
                         delimiter=' ', dtype=None)
#elements = [(9, 'Be', 100.)]
for element in elements:
    if element[1] != 'H' and element[1] != 'He':
        input = t(Z=element[1], A=element[0],
                  energy=np.linspace(0.0, 7.0, 100),
                  projectile='g', ejectile='n')
        input.run()
        input.proc_output(addtl_rxns=['fission'])
        sigma = f.curve(input.E, input.sigma,
                        name=r'%s-%d $\sigma_{\left(\gamma, n\right)}$' % \
                            (element[1], element[0]))
        sa = copy.deepcopy(sigma) * spectrum
        xs = sa.integrate(0., 6.)
        if np.max(input.sigma > 0.0) and input.Q > -6.:
            print '(g,n) %3s-%3d: Q = %10f | abundance = %10f | xs = %10f' % \
                (element[1], element[0], input.Q, element[2],
                 xs)
            plot = sigma.plot(linecolor=puc.brand_primary, linestyle='-')
            plot.legend()
            plot.xlabel(r'Energy ($E$) [$MeV$]')
            plot.ylabel(r'$\left( \gamma, n \right)$ Cross Section ($\sigma$) ' +
                        r'[$mb$]');
            plot.lines_on()
            plot.markers_off()
            plot.export('%s_%d_g_n' % (element[1], element[0]),
                        formats=['pdf'], sizes=['cs'],
                        customsize=(6, 4))
        if 'fission' in input.rxns:
            for E, sigma in zip(input.rxns['fission'][0],
                                input.rxns['fission'][1]):
                if sigma > 0.0:
                    fission_E = E
                    fission_sigma = E
                    break
            if fission_E < 6.0:
                curve = f.curve(input.rxns['fission'][0],
                                input.rxns['fission'][1],
                                name=r'$\sigma_{\left(f, n\right)}$')
                curve = curve * spectrum
                xs = curve.integrate(0., 6.)
                print '(g,f) %3s-%3d: Q = %10f | abundance = %10f | xs = %10f' % \
                    (element[1], element[0], -fission_E, element[2],
                     xs)

        input.clean()
