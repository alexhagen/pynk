import gamma

class hpge_file(gamma.gspectra):
    ''' a class for reading generalized hpge files
    '''
    def __init__(self, x, y, name):
        super(hpge_file, self).__init__(x=x, y=x, name=name)

class gammavision_file(hpge_file):
    ''' a glass for reading gammavision csv files
    '''
    def __init__(self, filename, name, prefix='../../enrichment/'):
        with open( + filename, 'r') as f:
            for i in range(11):
                f.readline()
            string = f.readline()
            bin1 = int(string.split()[0])
            bin2 = int(string.split()[1])
            ch = []
            cnt = []
            for i in range(bin1, bin2 + 1):
                channel = float(i)
                ch.extend([0.3854 + 0.254189 * channel + 4.29506e-8 * channel * channel])
                cnt.extend([float(f.readline())])
            super(gammavision_file, self).__init__(x=ch, y=cnt, name=name)
