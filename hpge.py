import gamma
import numpy as np

class hpge(gamma.gspectra):
    ''' a class for reading generalized hpge files
    '''
    def __init__(self, **kwargs):
        super(hpge, self).__init__(**kwargs)

class gammavision(hpge):
    ''' a class for reading gammavision csv files
    '''
    def __init__(self, filename, name=None, calib=[0., 1., 0.]):
        self.calib = calib
        self.fname = filename
        with open(filename, 'r') as f:
            for i in range(11):
                f.readline()
            string = f.readline()
            bin1 = int(string.split()[0])
            bin2 = int(string.split()[1])
            ch = []
            cnt = []
            for i in range(bin1, bin2 + 1):
                channel = float(i)
                ch.extend([self.calib[0] + self.calib[1] * channel + \
                    self.calib[2] * channel * channel])
                cnt.extend([float(f.readline())])
        super(gammavision, self).__init__(x=1000.0 * np.array(ch), y=cnt,
                                          name=name, calib=self.calib)
