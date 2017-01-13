import numpy as np
import itertools

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
        self.neutron_id = itertools.count().next()

    def add_event(self, n_event):
        self.events.append(n_event)
        self.num = len(self.events)

class cluster:
    def __init__(self):
        self.neutrons = []
        self.num = len(self.neutrons)
        self.cluster_id = itertools.count().next()

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
        return self

    def cut(self, Emin=0.0, Emax=np.inf):
        for curr_cluster in list(self.clusters):
            for curr_neutron in list(curr_cluster.neutrons):
                for curr_event in list(curr_neutron.events):
                    if curr_event.enreco > Emax or curr_event < Emin:
                        curr_neutron.events.remove(curr_event)
                if len(curr_neutron.events) == 0:
                    curr_cluster.neutrons.remove(curr_neutron)
            if len(curr_cluster.neutrons) == 0:
                self.clusters.remove(curr_cluster)

        self.neutrons = []
        self.events = []
        for curr_cluster in self.clusters:
            for curr_neutron in curr_cluster.neutrons:
                for curr_event in curr_neutron.events:
                    self.events.append(curr_event)
                self.neutrons.append(curr_neutron)
        return self

    def time_distribute(self, source, I):
        if source in ["Pu-Be", "PuBe", "Am-Be", "AmBe", "Po-Be", "PoBe"]:
            self.clusters = []
            # find the total time simulated
            total_t = float(len(self.neutrons)) / float(I)
            # time distribution
            time_dist = np.random.uniform(0, total_t, len(self.neutrons))
            time_dist.sort()
            # now we distribute each neutron randomly during that time window
            for rand_t, curr_neutron in zip(time_dist, self.neutrons):
                # take the random time and add it to the events in the n
                for n_event in curr_neutron.events:
                    n_event.t = n_event.t + rand_t
                # create a new cluster with one neutron in it
                curr_cluster = cluster()
                curr_cluster.add_neutron(curr_neutron)
                self.clusters.append(curr_cluster)
        elif source in ["Cf", "Cf-252", "252Cf"]:
            multiplicity = {0: 0.0034897361831755513,
                            1: 0.027817501375047515,
                            2: 0.12601897757999314,
                            3: 0.27501692366274216,
                            4: 0.30593530160659405,
                            5: 0.18711868872384044,
                            6: 0.06863045259258976,
                            7: 0.017099822686169885,
                            8: 0.0051417164440307195};
            nu_timeline = []
            for n, p in multiplicity.iteritems():
                nu_timeline.append(np.sum(nu_timeline) + p)
            nu_timeline = np.array(nu_timeline)
            avg_nu = np.sum([ float(n)*p for n, p in multiplicity.iteritems() ])
            self.clusters = []
            # find the total time simulated
            total_t = float(len(self.neutrons)) / (float(I) / avg_nu)
            # time distribution
            time_dist = np.random.uniform(0, total_t, len(self.neutrons))
            time_dist.sort()
            n_i = 0
            # now we distribute each fission event randomly in that time window
            while n_i < len(self.neutrons):
                # take the random time from the time distribution
                rand_t = time_dist[n_i]
                # create a new cluster, which is a fission
                curr_cluster = cluster()
                # choose a value from the multiplicity distribution
                n_n = (np.abs(nu_timeline-np.random.uniform())).argmin()
                for i in range(n_n):
                    if (n_i >= len(self.neutrons)):
                        break
                    curr_neutron = self.neutrons[n_i]
                    # take the random time and add it to the events in the n
                    for n_event in curr_neutron.events:
                        n_event.t = n_event.t + rand_t
                    # add this neutron to the current cluster
                    curr_cluster.add_neutron(curr_neutron)
                    n_i = n_i + 1
                # add the current cluster to the list of clusters
                self.clusters.append(curr_cluster)
