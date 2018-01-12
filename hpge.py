import gamma
import numpy as np
from pym import func as pym

class hpge(gamma.gspectra):
    ''' a class for reading generalized hpge files
    '''
    def __init__(self, **kwargs):
        super(hpge, self).__init__(**kwargs)

class gammavision(hpge):
    ''' a class for reading gammavision csv files
    '''
    def __init__(self, filename, name=None, calib=None):
        self.fname = filename
        E, cnt, calib = self.load_spe(filename, calib=calib)
        self.calib = calib
        spectrum = pym.curve(E, cnt, filename.replace('../', ''))
        super(gammavision, self).__init__(x=np.array(E), y=np.array(cnt),
                                          name=name, calib=self.calib)

    def load_spe(self, fname, calib=None):
        with open(fname, 'r') as f:
            for i in range(11):
                f.readline()
            string = f.readline()
            bin1 = int(string.split()[0])
            bin2 = int(string.split()[1])
            ch = []
            cnt = []
            for i in range(bin1, bin2 + 1):
                channel = float(i)
                ch.extend([channel])
                cnt.extend([float(f.readline())])
            line = ''
            while 'Live Time' not in line:
                line = f.readline()
            self.live_time = float(f.readline())
            while '$MCA_CAL' not in line:
                line = f.readline()
            cal_deg = int(f.readline())
            cal_line = f.readline().split()
            if calib is None:
                calib = [float(x) for x in cal_line[:-1]]
                calib = [1.0E-3 * x for x in calib]
        # convert the data given the calibration in the file
        if all(v == 0.0 for v in calib):
            print "no calibration"
            return ch, cnt, []
        elif len(calib) == 3:
            E = [calib[0] + calib[1] * _ch + calib[2] * _ch * _ch for _ch in ch]
        elif len(calib) == 2:
            E = [calib[0] + calib[1] * _ch for _ch in ch]
        elif len(calib) == 4:
            E = [calib[0] + calib[1] * _ch + calib[2] * _ch * _ch + calib[3] * _ch * _ch * _ch for _ch in ch]
        return E, cnt, calib
