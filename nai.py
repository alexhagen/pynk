from pym import func as pym

class nai_file(pym.curve):
    def __init__(self, filename, name, y_err=True, bf3_file=None, no_I=True,
                 I_scale=1.0, coeffs=None, prefix='../../enrichment/'):
        bins, counts = np.loadtxt(prefix + filename, delimiter=',', usecols=(0,2),
                                  unpack=True, skiprows=23)
        if y_err and coeffs is None:
            super(nai_file, self).__init__(x=bins, y=counts,
                                             u_y=np.sqrt(counts), name=name)
        elif not y_err and coeffs is None:
            super(nai_file, self).__init__(x=bins, y=counts, name=name)
        elif coeffs is not None:
            super(nai_file, self) \
                .__init__(x= coeffs[0] * np.power(np.array(bins), 2.0) + coeffs[1] * np.array(bins) + coeffs[2],
                          y=counts, name=name)
        with open(prefix + filename, 'r') as f:
            for i in range(13):
                f.readline()
            self.t = float(f.readline().replace('Live Time Elapsed:,', ''))
            self.start = \
                datetime.strptime(f.readline().replace('Start Time:,', ''),
                                  '%A, %B %d, %Y, %H:%M:%S\n') \
                                  - timedelta(minutes=22)
            self.stop = \
                datetime.strptime(f.readline().replace('End Time:,', ''),
                                  '%A, %B %d, %Y, %H:%M:%S\n') - \
                                  timedelta(minutes=22)
            if not no_I:
                self.I = I_scale * pys.bf3(bf3_file,
                                           start=self.start, stop=self.stop)
                self.name = name + ((r', $\bar{I}=%.1e}$')% self.I)\
                    .replace(r'e-0', r'\times 10^{-').replace(r'e+0', r'\times 10^{')
