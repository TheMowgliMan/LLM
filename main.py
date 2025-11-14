from math import *

class Neuron:
    inp = []
    wei = []
    out = 0
    __lastOut__ = 0

    def __init__(self, inputs, weights = []):
        if not isinstance(inputs, list):
            raise TypeError("Improper inputs format: must be of type 'list'")
        if not isinstance(weights, list):
            raise TypeError("Improper weights format: must be of type 'list'")
        if len(weights) != len(inputs) and weights != []:
            raise ValueError("Length of weights must match length of inputs")
        
        self.inp = inputs
        if weights == []:
            for i in range (len(self.inp)):
                self.wei.append(0)
        else:
            self.wei = weights

    def cycle