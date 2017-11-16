from pym import func as pym
import hpge as hpge
import glob
import re
from pyg.colors import pu as puc
import numpy as np

def get_date(filename):
    m = re.search('/*_([0-9]{2}_[0-9]{2}_[0-9]{2}).Spe', filename)
    if m:
        date = m.group(1)
    return date

class gspectra(pym.curve):
    ''' A generalized object for gamma spectra
    '''
    def __init__(self, x, y, name, calib=[0.0, 1.0E-3, 0.0]):
        self.calib = calib
        self.det = name
        super(gspectra, self).__init__(x=x, y=y, name=name)

    def background(self, fname_bkg):
        self.fname_bkg = fname_bkg
        self.bkg = hpge.gammavision(filename=fname_bkg,
                                    name='%s: bkg' % self.det,
                                    calib=self.calib)
        return self

    def comp_isotopes(self, adjust_calibration=False, plot_peaks=False,
                      plot_eff=False, plot_minimization=False):
        if adjust_calibration:
            # first, take the suggested calibration
            uhpre = hpge.gammavision(self.fname, name=self.det, calib=self.calib)
            bkgpre = hpge.gammavision(self.fname_bkg, name=self.det + ': bkg', calib=self.calib)
            uhmbkgsc = uhpre - bkgpre
            # plot the 185.72 keV U235 peak and find it's central location by fitting a gaussian
            lpk = uhmbkgsc.copy().crop(x_min=175., x_max=190., replace='remove')
            lpk.fit_gauss((1.0, 185.72, 1.))

            # plot the 742.80 keV U238 peak and find it's central location by fitting a gaussian
            mpk = uhmbkgsc.copy().crop(x_min=750., x_max=780., replace='remove')
            mpk.fit_gauss((1.0, 766.50, 1.))

            # plot the 1001.40 keV U238 peak and find its central location by fitting a gaussian
            hpk = uhmbkgsc.copy().crop(x_min=975., x_max=1025., replace='remove')
            hpk.fit_gauss((1.0, 1001.40, 1.))
            # calculate the new calibration and set these to the calibration
            newcalib = pym.curve([185.72, 766.50, 1001.40], [lpk.coeffs[1], mpk.coeffs[1], hpk.coeffs[1]])
            newcalib.fit_square()
            self.calib = self.calib * newcalib.coeffs
        # Now reimport with the new calibrations
        uh = hpge.gammavision(self.fname, name=self.det, calib=self.calib)
        bkg = hpge.gammavision(self.fname_bkg, name=self.det + ': bkg', calib=self.calib)
        uhmbkg = uh - bkg
        uhharry = uhmbkg.copy()
        E_238 = [0.06333, 0.25830, 0.74280, 0.76650, 1.00140]
        date = get_date(self.fname)
        if date == '10_31_17':
            low_238 = [60., 255., 740., 765., 998.]
            high_238 = [67.5, 260.5, 750., 774., 1011.]
        elif date == '11_02_17':
            low_238 = [59., 251., 732., 755., 991.]
            high_238 = [64.5, 256., 740., 764., 996.]
        elif date == '11_03_17':
            low_238 = [62., 257.5, 745., 767.5, 1002.]
            high_238 = [65., 262.5, 752.5, 780., 1015.]
        elif date == '11_07_17':
            low_238 = [62., 257.5, 743., 767.5, 1002.]
            high_238 = [65., 262.5, 753., 777.5, 1015.]
        elif date == '11_13_17':
            low_238 = [60., 255., 737., 760., 995.]
            high_238 = [64., 260., 745., 770., 1005.]
        else:
            low_238 = [62., 256.5, 739.5, 762.5, 996.]
            high_238 = [65., 259., 743., 766.5, 1002.]
        gamma_238 = [0.0425, 0.000770, 0.000870, 0.00343, 0.00889]
        peak238_nos = []
        for pk_E, low_E, high_E in zip(E_238, low_238, high_238):
            section = uhharry.copy().crop(x_min=pk_E * 1000. - 10., x_max=pk_E * 1000. + 10., replace='remove')
            peak = uhharry.copy().crop(x_min=low_E, x_max=high_E, replace='remove')
            peak.data = 'binned'
            bkg_cnts = (peak.x[-1] - peak.x[0]) * (peak.y[-1] + peak.y[0]) / 2.0
            deltax = peak.x[1] - peak.x[0]
            peak238_nos.extend([np.sum(peak.y * deltax) - bkg_cnts])
            if plot_peaks:
                plot = section.plot(linecolor=puc.pu_colors['blue'])
                plot.fill_between(peak.x, np.zeros_like(peak.x), peak.y, fc=puc.pu_colors['lightlightgray'])
                plot.semi_log_y()
                plot.markers_off()
                plot.export('../img/pk_%f' % pk_E, ratio='golden', sizes=['2'], force=True)
                plot.show('', label='')
                plot.close()
        E_235 = [0.14378, 0.16336, 0.18572, 0.20213, 0.20531]
        low_235 = [142., 161.5, 183.5, 200., 203.5]
        high_235 = [145.5, 165., 188., 203.5, 207.]
        gamma_235 = [0.1067, 0.0506, 0.576, 0.0108, 0.0494]
        E_235 = [0.14378, 0.16336, 0.18572]
        if date == '10_31_17':
            low_235 = [140., 160., 180.]
            high_235 = [146., 165.5, 190.]
        elif date == '11_02_17':
            low_235 = [138., 158., 180.]
            high_235 = [145., 163., 187.]
        elif date == '11_03_17':
            low_235 = [141., 162., 184.]
            high_235 = [147.5, 167.5, 190.]
        elif date == '11_07_17':
            low_235 = [141., 162., 183.]
            high_235 = [147.5, 167.5, 190.]
        elif date == '11_13_17':
            low_235 = [140., 160., 180.]
            high_235 = [146., 165., 189.]
        else:
            low_235 = [141., 160., 183.5]
            high_235 = [145.5, 165., 188.]
        gamma_235 = [0.1067, 0.0506, 0.576]
        peak235_nos = []
        for pk_E, low_E, high_E in zip(E_235, low_235, high_235):
            section = uhharry.copy().crop(x_min=pk_E * 1000. - 10., x_max=pk_E * 1000. + 10., replace='remove')
            peak = uhharry.copy().crop(x_min=low_E, x_max=high_E, replace='remove')
            peak.data = 'binned'
            bkg_cnts = (peak.x[-1] - peak.x[0]) * (peak.y[-1] + peak.y[0]) / 2.0
            deltax = peak.x[1] - peak.x[0]
            peak235_nos.extend([np.sum(peak.y * deltax) - bkg_cnts])
            if plot_peaks:
                plot = section.plot(linecolor=puc.pu_colors['red'])
                plot.fill_between(peak.x, np.zeros_like(peak.x), peak.y, fc=puc.pu_colors['lightlightgray'])
                plot.markers_off()
                plot.semi_log_y()
                plot.export('../img/pk_%f' % pk_E, force=True)
                plot.show('', label='')
                plot.close()
        Eas = []
        epsas = []
        for E_peak, R_peak, g235 in zip(E_235, peak235_nos, gamma_235):
            Eas.extend([np.log(E_peak)])
            epsas.extend([np.log(R_peak / g235)])
        epsa235 = pym.curve(Eas, epsas, '$U_{235}$')
        Eas = []
        epsas = []
        for E_peak, R_peak, g238 in zip(E_238, peak238_nos, gamma_238):
            Eas.extend([np.log(E_peak)])
            epsas.extend([np.log(R_peak / g238)])
        epsa238 = pym.curve(Eas, epsas, '$U_{238}$')
        epsa235.fit_square()
        epsa238.fit_square()
        if plot_eff:
            plot = epsa235.plot()
            plot = epsa235.plot_fit(addto=plot)
            plot = epsa238.plot(addto=plot)
            plot = epsa238.plot_fit(linestyle='--', addto=plot)
            plot.add_arrow(np.log(0.175), np.log(0.175), 13.2, 12.9, r'$\log\left(\varepsilon \cdot A_{235} \cdot k\right)$')
            plot.lines_off()
            plot.fit_lines_on()
            plot.legend(exclude='fit')
            plot.yticks([], [])
            plot.ylabel(r'Log Relative Efficiency-Activity ($\log \left( \varepsilon \cdot A \right)$) [ ]')
            plot.xlabel(r'Log Energy ($\log \left( E \right)$) [ ]')
            plot.export('eff', force=True)
            plot.show('', label='')
        lambda235 = np.log(2.0) / 2.22E16
        lambda234 = np.log(2.0) / (6.7 * 60. * 60.)
        lambda238 = np.log(2.0) / 1.409e17
        e_high = 0.25
        k_high = (lambda234/lambda235)*(1.0/e_high - 1.0)
        e_low = 1.0e-4
        k_low = (lambda234/lambda235)*(1.0/e_low - 1.0)
        Ss = []
        ks = np.exp(np.linspace(-1.0, 5.0, 5000))
        for k in ks:
            epsa = epsa238.copy()
            epsa.add_data(epsa235.x, epsa235.y + np.log(k))
            epsa.fit_square()
            e = 1.0 / (1.0 + k * (lambda235/lambda238))
            epsa.name = '%g' % e
            S_i = 0.0
            for X_i in epsa.x:
                S_i += np.power(epsa.fit_at(X_i) - epsa.at(X_i), 2.0)
            Ss.extend([np.sqrt(S_i)])
        if not np.isnan(Ss).all():
            S = pym.curve(ks, Ss)
            k_final = S.find_min()
            #print "k_final is %g" % k_final
            e = 1.0 / (1.0 + k_final * (lambda235/lambda238))
            #print "Enrichment is %g" % (e)
            return e[0]
        if plot_minimization:
            plot = S.plot()
            plot.markers_off()
            plot.export('svsk%s' % fname.replace('.Spe', '').replace('../', ''))
            plot.show('', label='')
            plot.close()

    def calc_enrichment_harry(self, fname, fname_bkg, calib=[0., 1.E-3, 0.]):
        # first, take the suggested calibration
        uhpre = hpge.gammavision(filename=fname, name='hpge', calib=calib)
        bkgpre = hpge.gammavision(filename=fname_bkg, name='hpge: bkg', calib=calib)
        uhmbkgsc = uhpre - bkgpre
        # plot the 185.72 keV U235 peak and find it's central location by fitting a gaussian
        lpk = uhmbkgsc.copy().crop(x_min=175., x_max=190., replace='remove')
        lpk.fit_gauss((1.0, 185.72, 1.))

        # plot the 742.80 keV U238 peak and find it's central location by fitting a gaussian
        mpk = uhmbkgsc.copy().crop(x_min=750., x_max=780., replace='remove')
        mpk.fit_gauss((1.0, 766.50, 1.))

        # plot the 1001.40 keV U238 peak and find its central location by fitting a gaussian
        hpk = uhmbkgsc.copy().crop(x_min=975., x_max=1025., replace='remove')
        hpk.fit_gauss((1.0, 1001.40, 1.))
        # calculate the new calibration and set these to the calibration
        newcalib = pym.curve([185.72, 766.50, 1001.40], [lpk.coeffs[1], mpk.coeffs[1], hpk.coeffs[1]])
        newcalib.fit_square()
        newcalibconstants = calib#newcalib.coeffs * calib
        # Now reimport with the new calibrations
        uh = hpge.gammavision(filename=fname, name='hpge', calib=newcalibconstants)
        bkg = hpge.gammavision(filename=fname_bkg, name='hpge: bkg', calib=newcalibconstants)
        uhmbkg = uh - bkg
        uhharry = uhmbkg.copy()
        E_238 = [0.06333, 0.25830, 0.74280, 0.76650, 1.00140]
        date = get_date(fname)
        if date == '10_31_17':
            low_238 = [60., 255., 740., 765., 998.]
            high_238 = [67.5, 260.5, 750., 774., 1011.]
        elif date == '11_02_17':
            low_238 = [59., 251., 732., 755., 991.]
            high_238 = [64.5, 256., 740., 764., 996.]
        elif date == '11_03_17':
            low_238 = [62., 257.5, 745., 767.5, 1002.]
            high_238 = [65., 262.5, 752.5, 780., 1015.]
        elif date == '11_07_17':
            low_238 = [62., 257.5, 743., 767.5, 1002.]
            high_238 = [65., 262.5, 753., 777.5, 1015.]
        elif date == '11_13_17':
            low_238 = [60., 255., 737., 760., 995.]
            high_238 = [64., 260., 745., 770., 1005.]
        else:
            low_238 = [62., 256.5, 739.5, 762.5, 996.]
            high_238 = [65., 259., 743., 766.5, 1002.]
        gamma_238 = [0.0425, 0.000770, 0.000870, 0.00343, 0.00889]
        #E_238 = [0.74280, 0.76650, 1.00140]
        #low_238 = [739.5, 762.5, 996.]
        #high_238 = [743., 766.5, 1002.]
        #gamma_238 = [0.000870, 0.00343, 0.00889]
        peak238_nos = []
        for pk_E, low_E, high_E in zip(E_238, low_238, high_238):
            section = uhharry.copy().crop(x_min=pk_E * 1000. - 10., x_max=pk_E * 1000. + 10., replace='remove')
            plot = section.plot(linecolor=puc.pu_colors['blue'])
            peak = uhharry.copy().crop(x_min=low_E, x_max=high_E, replace='remove')
            peak.data = 'binned'
            bkg_cnts = (peak.x[-1] - peak.x[0]) * (peak.y[-1] + peak.y[0]) / 2.0
            deltax = peak.x[1] - peak.x[0]
            peak238_nos.extend([np.sum(peak.y * deltax) - bkg_cnts])
            plot.fill_between(peak.x, np.zeros_like(peak.x), peak.y, fc=puc.pu_colors['lightlightgray'])
            #plot.ylim(0., np.max(peak.y))
            plot.semi_log_y()
            plot.markers_off()
            plot.export('../img/pk_%f' % pk_E, ratio='golden', sizes=['2'], force=True)
            plot.show('', label='')
            plot.close()
        E_235 = [0.14378, 0.16336, 0.18572, 0.20213, 0.20531]
        low_235 = [142., 161.5, 183.5, 200., 203.5]
        high_235 = [145.5, 165., 188., 203.5, 207.]
        gamma_235 = [0.1067, 0.0506, 0.576, 0.0108, 0.0494]
        E_235 = [0.14378, 0.16336, 0.18572]

        if date == '10_31_17':
            low_235 = [140., 160., 180.]
            high_235 = [146., 165.5, 190.]
        elif date == '11_02_17':
            low_235 = [138., 158., 180.]
            high_235 = [145., 163., 187.]
        elif date == '11_03_17':
            low_235 = [141., 162., 184.]
            high_235 = [147.5, 167.5, 190.]
        elif date == '11_07_17':
            low_235 = [141., 162., 183.]
            high_235 = [147.5, 167.5, 190.]
        elif date == '11_13_17':
            low_235 = [140., 160., 180.]
            high_235 = [146., 165., 189.]
        else:
            low_235 = [141., 160., 183.5]
            high_235 = [145.5, 165., 188.]
        gamma_235 = [0.1067, 0.0506, 0.576]
        peak235_nos = []
        for pk_E, low_E, high_E in zip(E_235, low_235, high_235):
            section = uhharry.copy().crop(x_min=pk_E * 1000. - 10., x_max=pk_E * 1000. + 10., replace='remove')
            plot = section.plot(linecolor=puc.pu_colors['red'])
            peak = uhharry.copy().crop(x_min=low_E, x_max=high_E, replace='remove')
            peak.data = 'binned'
            bkg_cnts = (peak.x[-1] - peak.x[0]) * (peak.y[-1] + peak.y[0]) / 2.0
            deltax = peak.x[1] - peak.x[0]
            peak235_nos.extend([np.sum(peak.y * deltax) - bkg_cnts])
            plot.fill_between(peak.x, np.zeros_like(peak.x), peak.y, fc=puc.pu_colors['lightlightgray'])
            plot.markers_off()
            plot.semi_log_y()
            plot.export('../img/pk_%f' % pk_E, force=True)
            plot.show('', label='')
            plot.close()
        Eas = []
        epsas = []
        for E_peak, R_peak, g235 in zip(E_235, peak235_nos, gamma_235):
            Eas.extend([np.log(E_peak)])
            epsas.extend([np.log(R_peak / g235)])
        epsa235 = pym.curve(Eas, epsas, '$U_{235}$')
        Eas = []
        epsas = []
        for E_peak, R_peak, g238 in zip(E_238, peak238_nos, gamma_238):
            Eas.extend([np.log(E_peak)])
            epsas.extend([np.log(R_peak / g238)])
        epsa238 = pym.curve(Eas, epsas, '$U_{238}$')
        plot = epsa235.plot()
        epsa235.fit_square()
        plot = epsa235.plot_fit(addto=plot)
        plot = epsa238.plot(addto=plot)
        epsa238.fit_square()
        plot = epsa238.plot_fit(linestyle='--', addto=plot)
        plot.add_arrow(np.log(0.175), np.log(0.175), 13.2, 12.9, r'$\log\left(\varepsilon \cdot A_{235} \cdot k\right)$')
        plot.lines_off()
        plot.fit_lines_on()
        plot.legend(exclude='fit')
        plot.yticks([], [])
        plot.ylabel(r'Log Relative Efficiency-Activity ($\log \left( \varepsilon \cdot A \right)$) [ ]')
        plot.xlabel(r'Log Energy ($\log \left( E \right)$) [ ]')
        plot.export('eff', force=True)
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
        #plot.close()
        if not np.isnan(Ss).all():
            S = pym.curve(ks, Ss)
            print S.x, S.y
            k_final = S.find_min()
            print "k_final is %g" % k_final
            e = 1.0 / (1.0 + k_final * (lambda235/lambda238))
            print "Enrichment is %g" % (e)
        plot = S.plot()
        plot.markers_off()
        plot.export('svsk%s' % fname.replace('.Spe', '').replace('../', ''))
        plot.show('', label='')
        plot.close()
