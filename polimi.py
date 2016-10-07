import numpy as np

class event:
    def __init__(self, polimi_string):
        # convert the str to a string object
        arr = polimi_string.split()
        # now parse out all of those numbers
        self.nps = int(arr[0])
        self.npar = int(arr[1])
        self.ipt = int(arr[2])
        # collision type
        ntyn = int(arr[3])
        # covert collision type to plaintext
        if (ntyn == 0):
          self.collision_type = 'collision'
        elif (ntyn == -99):
          self.collision_type = 'elastic'
        elif (ntyn == 99):
          self.collision_type = 'sab collision'
        elif (ntyn == 1 or ntyn == -1):
          self.collision_type = 'inelastic'
        elif (ntyn == 19):
          self.collision_type = 'fission'
        else:
          self.collision_type = '(n,%in)' % (np.sqrt(ntyn**2))
        self.nxs = int(arr[4])
        self.ncl = int(arr[5])
        self.enreco = float(arr[6])
        # time in shakes
        tme = float(arr[7])
        # convert shakes to seconds
        self.t = tme * 10.**-8.
        self.xxx = float(arr[8])
        self.yyy = float(arr[9])
        self.zzz = float(arr[10])
        self.wgt = float(arr[11])
        self.ngen = int(arr[12])
        self.nsca = int(arr[13])
        self.ncode = int(arr[14])
        self.erg = float(arr[15])

    def pretty_print(self):
        print ("Neutron %i had interaction: " +
            "%s with nucleus %i at " +
            "(%f, %f, %f) at time %e s") % (self.nps, self.collision_type,
                                            self.nxs, self.xxx, self.yyy,
                                            self.zzz, self.t)

class neutron:
    def __init__(self):
        self.events = []
        self.num = len(self.events)

    def add_event(self, n_event):
        self.events.append(n_event)
        self.num = len(self.events)

class cluster:
    def __init__(self):
        self.neutrons = []
        self.num = len(self.neutrons)

    def add_neutron(self, c_neutron):
        self.neutrons.append(c_neutron)
        self.num = len(self.neutrons)

class polimi:
    def __init__(self):
        self.events = []
        self.neutrons = []
        self.clusters = []

    def import_polimi_file(self, filename):
        f = open(filename, 'r')

        for line in f:
            n_event = event(line)
            self.events.append(n_event)

        # now we need to split everything into neutrons
        curr_nps = 1
        curr_neutron = neutron()
        for n_event in self.events:
            if (n_event.nps != curr_nps):
                self.neutrons.append(curr_neutron)
                curr_neutron = neutron()
                curr_neutron.add_event(n_event)
                curr_nps = n_event.nps
            else:
                curr_neutron.add_event(n_event)

        # before any time distribution, everything is in one single cluster
        # that was emitted at time 0
        curr_cluster = cluster()
        for n in self.neutrons:
            curr_cluster.add_neutron(n)

        self.clusters.append(curr_cluster)

        def time_distribute(self, source, I):
            if source in ["Pu-Be", "PuBe", "Am-Be", "AmBe", "Po-Be", "PoBe"]:
                dist = rand
            elif source in ["Cf", "Cf-252", "252Cf"]:
                dist = calif


            #self.clusters = []
            #for n in self.neutrons:
