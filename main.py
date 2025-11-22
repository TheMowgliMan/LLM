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

        # Process neuron, which is LReLU(tanh(inp[0] * wei[0], inp[1] * wei[1], [...] inp[x] * wei[x]))
        proc = tanh(sum([self.inp[i] * self.wei [i] if self.inp[i] * self.wei [i] > self.__tolerance__ else 0 for i in range(len(self.inp))]))
        proc = max(-0.01*abs(proc), proc) # TanH Leaky RelU

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
    boxes = []
    size = 0
    last_box = None

    # Size is the edge length of the number of intervening blocks between I and O
    def __init__(self, size:int) -> None:
        self.m = Memory()
        self.size = size
        self.boxes = []
        self.last_box = Box(size * 16, 1, 16)
        for i in range(size):
            side = [Box(size * 16, 48, 16) for y in range(size * 2)]
            self.boxes.append(side)

    def ai_spaghetti(self, word):
        pass

if __name__ == "__main__":
    langmod = LanguageModel(19)

    while True:
        prompt = input("?> ")

        if prompt.lower() == "end":
            break;
        else:
            prompt = prompt.split()
            if prompt[0] == "importf":
                try:
                    langmod.m.import_str(FileImporter.importf(prompt[1]))
                    print(str(len(langmod.m)) + " items in dataset")
                except IndexError:
                    print("'importf' requires 1 param: <file_name_or_path>")
                except FileNotFoundError:
                    print("File '", prompt[1], "' doesn't exist!")
            if prompt[0] == "spaghetti":
                try:
                    dat = prompt[1]
                    last = dat
                    last_idx = langmod.m.index(last)
                    two_idx = None
                    for i in range(int(prompt[2])):
                        if r.random() > 0.05 or i < 2:
                            idx = floor((len(langmod.m.get_all_refs_at_item(last_idx)) - 1) / 1)
                            f = r.randint(0, idx)
                            last = langmod.m.follow_ref(last_idx, f)
                            two_idx = last_idx
                            last_idx = langmod.m.get_ref(last_idx, f)[0]
                        else:
                            idx = floor((len(langmod.m.get_all_refs_at_item(two_idx, type=True)) - 1) / 1)
                            f = r.randint(0, idx)
                            last = langmod.m.follow_ref(two_idx, f, type=True)
                            tt = two_idx
                            two_idx = last_idx
                            last_idx = langmod.m.get_ref(tt, f, type=True)[0]
                        dat = dat + " " + last

                    print(dat)
                except IndexError:
                    print("'spaghetti' requires 2 params: <word>, <count>")