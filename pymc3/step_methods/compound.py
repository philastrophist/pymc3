'''
Created on Mar 7, 2011

@author: johnsalvatier
'''


class CompoundStep(object):
    """Step method composed of a list of several other step methods applied in sequence."""

    def __init__(self, methods):
        self.methods = list(methods)
        self.generates_stats = any(method.generates_stats for method in self.methods)
        self.stats_dtypes = []
        for method in self.methods:
            if method.generates_stats:
                self.stats_dtypes.extend(method.stats_dtypes)
        assert all(m.nparticles is None for m in methods), "CompoundStep is not for use with particlesteps"
        self.nparticles = None

    def step(self, point):
        if self.generates_stats:
            states = []
            for method in self.methods:
                if method.generates_stats:
                    point, state = method.step(point)
                    states.extend(state)
                else:
                    point = method.step(point)
            return point, states
        else:
            for method in self.methods:
                point = method.step(point)
            return point


# TODO: Compound Particle steps with other particlesteps / with other scalar steps (create particlestep for each) (may be expensive)