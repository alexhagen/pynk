import gamma
import numpy as np

class hpge(gamma.gspectra):
    ''' a class for reading generalized hpge files
    '''
    def __init__(self, x, y, name):
        super(hpge, self).__init__(x=x, y=x, name=name)

class gammavision(hpge):
    ''' a glass for reading gammavision csv files
    '''
    def __init__(self, filename, name=None, calib_const=[0., 1., 0.]):
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
                ch.extend([calib_const[0] + calib_const[1] * channel + \
                    calib_const[2] * channel * channel])
                cnt.extend([float(f.readline())])
            super(gammavision, self).__init__(x=1000.0 * np.array(ch), y=cnt,
                                              name=name)
