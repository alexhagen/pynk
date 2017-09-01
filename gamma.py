from pym import func as pym

class gspectra(pym.curve):
    ''' A generalized object for gamma spectra
    '''
    def __init__(self, x, y, name):
        super(gspectra, self).__init__(x=x, y=x, name=name)

    def calc_enrichment_harry(self):
        ''' Implementation of Harry and Adlik's 1986 method for determination
            of Uranium enrichment without the use of standards
        '''
        E_238 = [0.06333, 0.25830, 0.74280, 0.76650, 1.00140]
        low_238 = [62., 256.5, 739.5, 762.5, 996.]
        high_238 = [65., 259., 743., 766.5, 1002.]
        gamma_238 = [0.0425, 0.000770, 0.000870, 0.00343, 0.00889]
        peak238_nos = []
        for pk_E, low_E, high_E in zip(E_238, low_238, high_238):
            #print uhharry.at(pk_E * 1000.)
            plot = uhharry.copy().crop(x_min=pk_E * 1000. - 10., x_max=pk_E * 1000. + 10., replace='remove')\
                .plot(linecolor=puc.pu_colors['blue'])
            peak = uhharry.copy().crop(x_min=low_E, x_max=high_E, replace='remove')
            peak.data = 'binned'
            bkg = (peak.x[-1] - peak.x[0]) * (peak.y[-1] + peak.y[0]) / 2.0
            deltax = peak.x[1] - peak.x[0]
            peak238_nos.extend([np.sum(peak.y * deltax) - bkg])
            #plot.fill_between(peak.x, np.zeros_like(peak.x), peak.y, fc=puc.pu_colors['lightlightgray'])
            #plot.ylim(0., np.max(peak.y))
            #plot.markers_off()
            #plot.export('../img/pk_%f' % pk_E, force=True)
            #plot.show('', label='')
            #plot.close()
        E_235 = [0.14378, 0.16336, 0.18572, 0.20213, 0.20531]
        low_235 = [142., 161.5, 183.5, 200., 203.5]
        high_235 = [145.5, 165., 188., 203.5, 207.]
        gamma_235 = [0.1067, 0.0506, 0.576, 0.0108, 0.0494]
        E_238 = [0.06333, 0.25830, 0.74280, 0.76650, 1.00140, 1.7385, 1.8319]
        gamma_238 = [0.0425, 0.000770, 0.000870, 0.00343, 0.00889]
        peak235_nos = []
        for pk_E, low_E, high_E in zip(E_235, low_235, high_235):
            plot = uhharry.copy().crop(x_min=pk_E * 1000. - 10., x_max=pk_E * 1000. + 10., replace='remove')\
                .plot(linecolor=puc.pu_colors['red'])
            peak = uhharry.copy().crop(x_min=low_E, x_max=high_E, replace='remove')
            peak.data = 'binned'
            bkg = (peak.x[-1] - peak.x[0]) * (peak.y[-1] + peak.y[0]) / 2.0
            #print peak.integrate()
            #print bkg
            deltax = peak.x[1] - peak.x[0]
            peak235_nos.extend([np.sum(peak.y * deltax) - bkg])
            #plot.fill_between(peak.x, np.zeros_like(peak.x), peak.y, fc=puc.pu_colors['lightlightgray'])
            #plot.markers_off()
            #plot.export('../img/pk_%f' % pk_E, force=True)
            #plot.show('', label='')
            #plot.close()
        Eas = []
        epsas = []
        for E_peak, R_peak, g235 in zip(E_235, peak235_nos, gamma_235):
            Eas.extend([np.log(E_peak)])
            epsas.extend([np.log(R_peak / g235)])
        epsa235 = ahf.curve(Eas, epsas, '$U_{235}$')
        Eas = []
        epsas = []
        for E_peak, R_peak, g238 in zip(E_238, peak238_nos, gamma_238):
            Eas.extend([np.log(E_peak)])
            epsas.extend([np.log(R_peak / g238)])
        epsa238 = ahf.curve(Eas, epsas, '$U_{238}$')
        plot = epsa235.plot()
        #epsa235.fit_square()
        #plot = epsa235.plot_fit(addto=plot)
        plot = epsa238.plot(addto=plot)
        epsa238.fit_square()
        plot = epsa238.plot_fit(linestyle='--', addto=plot)
        plot.add_arrow(np.log(0.175), np.log(0.175), 13.2, 12.9, r'$\log\left(\varepsilon \cdot A_{235} \cdot k\right)$')
        plot.lines_off()
        plot.fit_lines_on()
        plot.legend(exclude='fit')
        #plot.yticks([], [])
        plot.ylabel(r'Log Relative Efficiency-Activity ($\log \left( \varepsilon \cdot A \right)$) [ ]')
        plot.xlabel(r'Log Energy ($\log \left( E \right)$) [ ]')
        plot.export('eff')
        plot.show('', label='')
        lambda235 = np.log(2.0) / 2.22E16
        lambda234 = np.log(2.0) / (6.7 * 60. * 60.)
        lambda238 = np.log(2.0) / 1.409e17
        e_high = 0.25
        k_high = (lambda234/lambda235)*(1.0/e_high - 1.0)
        e_low = 1.0e-4
        k_low = (lambda234/lambda235)*(1.0/e_low - 1.0)
        #ks = np.linspace(k_low, k_high, 1000)
        Ss = []
        #plot = ahp.pyg2d()
        ks = np.exp(np.linspace(-1.0, 5.0, 5000))
        for k in ks:
            epsa = epsa238.copy()
            epsa.add_data(epsa235.x, epsa235.y + np.log(k))
            epsa.fit_square()
            e = 1.0 / (1.0 + k * (lambda235/lambda238))
            epsa.name = '%g' % e
            #plot = epsa.plot_fit(addto=plot)
            #plot = epsa.plot(addto=plot)
            S_i = 0.0
            for X_i in epsa.x:
                S_i += np.power(epsa.fit_at(X_i) - epsa.at(X_i), 2.0)
            Ss.extend([np.sqrt(S_i)])
        #plot.legend()
        #plot.lines_off()
        #plot.fit_lines_on()
        #plot.fit_markers_off()
        #plot.export('ks')
        #plot.show('', label='')
        S = ahf.curve(ks, Ss)
        k_final = S.find_min()
        print "k_final is %g" % k_final
        e = 1.0 / (1.0 + k_final * (lambda235/lambda238))
        print "Enrichment is %g" % (e)
        plot = S.plot()
        plot.markers_off()
        plot.export('svsk')
        plot.show('', label='')
