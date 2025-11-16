from math import *

class Neuron:
    inp = []
    wei = []
    out = 0
    __lastOut__ = 0
    __tolerance__ = 0.4
    __fired__ = False

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

    def run(self, inputs = []):
        if len(inputs) != len(inputs) and inputs != []:
            raise ValueError("Length of inputs must be zero or match the number of defined inputs")
        
        self.__fired__ = False
        # If there are no inputs, generate the proper number of input data to use
        if inputs != []: self.inp = inputs
        else: self.inp = [0] * len(self.inp)

        # Process neuron, which is tanh(inp[0] * wei[0], inp[1] * wei[1], [...] inp[x] * wei[x])
        proc = 0
        for i in range(len(self.inp)): proc += self.inp[i] * self.wei [i]
        proc = tanh(proc)
        # When the neuron is less than the tolerance + part of out, don't fire
        if abs(proc + self.out / 2) < self.__tolerance__:
            proc = 0
            self.out *= 0.80 # Out decays over time if it failed to fire
            self.__tolerance__ *= 1.0001 # Long disuse causes tolerance to increase
            return self.out 
        else: self.out = proc; self.__lastOut__ = proc; self.__fired__ = True # Fire!

        # It becomes desensitized to an input if it is far higher than any others
        getsorted = sorted(self.inp, reverse=True)
        if self.__fired__ == True and (abs(getsorted[0]) - abs(getsorted[1]) > 0.3):
            self.wei[self.inp.index(max(self.inp))] *= 0.9999 # Reduce the weight
        del getsorted # Just in case

        return self.out
    
    def get_fired(self):
        return self.__fired__
    
    def get_last_out(self):
        return self.__lastOut__

