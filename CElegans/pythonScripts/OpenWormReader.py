from NeuroMLUtilities import ConnectionInfo
import PyOpenWorm as P

import logging

############################################################

#   A simple script to read the values in PyOpenWorm
#   Originally written by Mark Watts (github.com/mwatts15)

############################################################

logger = logging.getLogger("OpenWormReader")

class OpenWormReader:
    def __init__(self):
        logger.info("Initialising OpenWormReader")
        P.connect()
        self.net = P.Worm().get_neuron_network()
        self.all_connections = self.net.synapses()
        self.neuron_connections = set(filter(lambda x: x.termination() == u'neuron', self.all_connections))
        self.muscle_connections = set(filter(lambda x: x.termination() == u'muscle', self.all_connections))
        logger.info("Finished initialising OpenWormReader")

    def read(self, include_nonconnected_cells=False):

        conns = []
        cells = []
        for s in self.neuron_connections:
            pre = str(s.pre_cell().name())
            post = str(s.post_cell().name())
            syntype = str(s.syntype())
            num = int(s.number())
            synclass = str(s.synclass())

            conns.append(ConnectionInfo(pre, post, num, syntype, synclass))

            if pre not in cells:
                cells.append(pre)
            if post not in cells:
                cells.append(post)

        known_nonconnected_cells = ['CANL', 'CANR', 'VC6']
        # ignore the cells unconnected if neuron_connect = True
        if(include_nonconnected_cells):
            for c in known_nonconnected_cells:
                # to avoid an exception: nonconnected cell becomes connected.
                if c not in cells:
                    cells.append(c)

        logger.info("Total cells read " + str(len(cells)))
        logger.info("Total connections read " + str(len(conns)))
        return cells, conns

    def readMuscleData(self):

        conns = []
        neurons = []
        muscles = []
        for s in self.muscle_connections:
            pre = str(s.pre_cell().name())
            post = str(s.post_cell().name())
            syntype = str(s.syntype())
            num = int(s.number())
            synclass = str(s.synclass())

            conns.append(ConnectionInfo(pre, post, num, syntype, synclass))

            if isinstance(s.post_cell(), P.Muscle) and post not in muscles:
                muscles.append(post)
            elif post not in neurons:
                neurons.append(post)

            if isinstance(s.pre_cell(), P.Muscle) and pre not in muscles:
                muscles.append(pre)
            elif post not in neurons:
                neurons.append(pre)

        logger.info("Total neurons connected to muscles read " + str(len(neurons)))
        logger.info("Total muscles connected to neurons read " + str(len(muscles)))
        logger.info("Total connections between neurons and muscles read " + str(len(conns)))

        return neurons, muscles, conns

    def finish(self):
        P.disconnect()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(name)s - %(levelname)s: %(message)s')
    owr = OpenWormReader()
    owr.read()
    owr.readMuscleData()
    owr.finish()
