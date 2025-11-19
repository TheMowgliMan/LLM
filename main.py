from math import *
from memory import *
import random as r

class Neuron:
    inp = []
    wei = []
    out = 0
    __lastOut__ = 0
    __tolerance__ = 0.1
    __fired__ = False

    def __init__(self, inputs : list, weights : list = []):
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

    def run(self, inputs:list = []):
        # print(len(self.inp), len(self.wei))

        if len(inputs) != len(self.inp) and inputs != []:
            raise ValueError("Length of inputs must be zero or match the number of defined inputs")
        
        self.__fired__ = False
        # If there are no inputs, generate the proper number of input data to use
        if inputs != []: self.inp = inputs
        else: self.inp = [0] * len(self.inp)

        # Process neuron, which is tanh(inp[0] * wei[0], inp[1] * wei[1], [...] inp[x] * wei[x])
        proc = 0
        for i in range(len(self.inp)):
            d = self.inp[i] * self.wei [i]
            if abs(d) > self.__tolerance__:
                proc += self.inp[i] * self.wei [i]
        proc = tanh(proc)

        # When the neuron is less than the tolerance + part of out, don't fire
        if abs(proc + self.out / 2) < self.__tolerance__:
            proc = 0
            self.out *= 0.80 # Out decays over time if it failed to fire
            self.__tolerance__ *= 1.00001 # Long disuse causes tolerance to increase
            return self.out 
        else: self.out = proc; self.__lastOut__ = proc; self.__fired__ = True # Fire!

        # It becomes desensitized to an input if it is far higher than any others
        if len(self.inp) > 1:
            getsorted = sorted(self.inp, reverse=True)
            if self.__fired__ == True and (abs(getsorted[0]) - abs(getsorted[1]) > 0.3):
                self.wei[self.inp.index(max(self.inp))] *= 0.99999 # Reduce the weight
            del getsorted # Just in case

        return self.out
    
    def get_fired(self):
        return self.__fired__
    
    def get_last_out(self):
        return self.__lastOut__
    
    # Encourages neurons that fired and discourages ones that didn't to force a certain outcome
    def train(self, target):
        raise NotImplementedError("This brain is lazy")
    
class Box:
    ns = []
    inp = 0
    outs = []
    def __init__(self, inputs:int, width:int, height:int):
        self.inp = inputs
        for x in range(width):
            line = []
            for y in range(height):
                if x == 0:
                    line.append(Neuron([0]*inputs, weights=[r.uniform(-5.0, 5.0) for _ in range(inputs)]))
                else:
                    line.append(Neuron([0]*height, weights=[r.uniform(-5.0, 5.0) for _ in range(height)]))
            self.ns.append(line)

        self.outs = [0] * height

    def run(self, inps:list):
        if len(inps) != self.inp:
            raise IndexError("Incorrect number on inputs to this box: input count must match definition; needed " + str(self.inp) + " not " + str(len(inps)) + ".")
        
        ix = 0
        last = []
        now = []
        print(len(self.ns))
        for x in self.ns:
            now = []
            for y in x:
                if ix == 0:
                    now.append(y.run(inputs=inps))
                else:
                    now.append(y.run(inputs=last))
            last = now.copy()
            ix += 1
            # print(last)
        
        self.outs = last
        return self.outs

if __name__ == "__main__":
    print("creating boxes")
    b = Box(3, 16, 2)
    box = Box(3, 16, 2)

    print("boxes created. processing...")
    b.run([0.3, -0.3, 0.7])
    box.run([0.3, -0.3, 0.7])

    print("done")