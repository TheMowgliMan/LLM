from math import * # pyright: ignore[reportWildcardImportFromLibrary]
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
    # members
    ns = []
    inp = 0
    outs = []

    def __init__(self, inputc:int, widthc:int, heightc:int):
        # Init local variables just to be safe
        self.ns = []
        self.inp = 0
        self.outs = []

        # The number of inputs this box has, added for verification purposes
        self.inp = inputc

        # Iterate for a number equal to the width to get every column
        for x in range(widthc):
            # Create empty column
            line = []
            for y in range(heightc):
                # If this is the first column...
                if x == 0:
                    # ...have number of inputs equal to box inputs...
                    line.append(Neuron([0]*inputc, weights=[r.uniform(-5.0, 5.0) for _ in range(inputc)]))
                else:
                    # ...otherwise equal to neuron inputs...
                    line.append(Neuron([0]*heightc, weights=[r.uniform(-5.0, 5.0) for _ in range(heightc)]))

            # Add the column to the box
            self.ns.append(line)

        self.outs = [0] * heightc

    def run(self, inps:list):
        if len(inps) != self.inp:
            raise IndexError("Incorrect number on inputs to this box: input count must match definition; needed " + str(self.inp) + " not " + str(len(inps)) + ".")
        
        ix = 0
        last = []
        now = []
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
    
class FileImporter:
    @staticmethod
    def importf(fname):
        try:
            f = open(fname, encoding="utf8")
            t = f.read()
        finally:
            f.close() # pyright: ignore[reportPossiblyUnboundVariable]
        return t

class LanguageModel:
    m = Memory()

    def __init__(self) -> None:
        self.m = Memory()

if __name__ == "__main__":
    langmod = LanguageModel()

    while True:
        prompt = input("?> ")

        if prompt.lower() == "end":
            break;
        else:
            prompt = prompt.split()
            if prompt[0] == "importf":
                try:
                    langmod.m.import_str(FileImporter.importf(prompt[1]))
                except IndexError:
                    print("'importf' requires 1 param: <file_name_or_path>")
                except FileNotFoundError:
                    print("File '", prompt[1], "' doesn't exist!")
            if prompt[0] == "spaghetti":
                try:
                    dat = prompt[1]
                    last = dat
                    for i in range(int(prompt[2])):
                        idx = floor((len(langmod.m.get_all_refs_at_item(langmod.m.index(last))) - 1) / 1)
                        last = langmod.m.follow_ref(langmod.m.index(last), r.randint(0, idx))
                        dat = dat + " " + last

                    print(dat)
                except IndexError:
                    print("'spaghetti' requires 2 params: <word>, <count>")