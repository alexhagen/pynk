from pynk.talys import talys as t
from pym import func as f
import numpy as np
import copy
from pyg.colors import pu as puc

input = t(Z='F', A=19,
          energy=np.linspace(0.0, 2.5, 10),
          projectile='n', ejectile='n', level=5)
input.run()
input.clean()
# input.proc_output(addtl_rxns=['fission'])
# sigma = f.curve(input.E, input.sigma,
#                 name=r'%s-%d $\sigma_{\left(\gamma, n\right)}$' % \
#                     (element[1], element[0]))
# plot = sigma.plot(linecolor=puc.brand_primary, linestyle='-')
# plot.legend()
# plot.xlabel(r'Energy ($E$) [$MeV$]')
# plot.ylabel(r'$\left( \gamma, n \right)$ Cross Section ($\sigma$) ' +
#             r'[$mb$]');
# plot.lines_on()
# plot.markers_off()
# plot.export('%s_%d_g_n' % (element[1], element[0]),
#             formats=['pdf'], sizes=['cs'],
#             customsize=(6, 4))
