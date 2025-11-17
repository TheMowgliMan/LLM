class Memory:
    items = []

    # Store references to items that are different in form but similar in meaning
    similar_ref = [] # Format: [[[idx1, count1], [idx2, count2], [...] [idxX, countX]], [[idx1, count1], [idx2, count2], [...] [idxX, countX]]]
    # Store references to items that are connected to this one
    connection_ref = [] # Format: [[[idx1, count1], [idx2, count2], [...] [idxX, countX]], [[idx1, count1], [idx2, count2], [...] [idxX, countX]]]

    def __getitem__(self, foo):
        if not isinstance(foo, tuple):
            return self.items[foo]
        elif foo[2] == False: # Similar reference
            try:
                return self.similar_ref[foo[0]][foo[1]]
            except IndexError:
                return []
        elif foo[2] == True: # Connection reference
            try:
                return self.connection_ref[foo[0]][foo[1]]
            except IndexError:
                return []
        else:
            raise IndexError("Improper indice to __getitem__: '" + str(foo) + "' is not valid!")
    
    def __setitem__(self, foo, datum):
        if not isinstance(foo, tuple):
            self.items[foo] = datum
        elif foo[2] == False and isinstance(datum, list) and len(datum) == 2: # Similar reference
            self.similar_ref[foo[0]][foo[1]] = datum
        elif foo[2] == True and isinstance(datum, list) and len(datum) == 2: # Connection reference
            self.connection_ref[foo[0]][foo[1]] = datum
        else:
            raise IndexError("Improper indice or datum to __setitem__: indice '" + str(foo) + "' and/or datum '" + str(datum) + "' are not valid!")
        
    def append(self, datum):
        self.items.append(datum)
        self.similar_ref.append([])
        self.connection_ref.append([])

if __name__ == "__main__":
    m = Memory()
    m.append("buh")
    print(m[0])
    print(m[0, 0, False])
    print(m[0, 0, True])
    m[0, 0, False] = [1, 2]
    m[0, 0, True] = [2, 3]
    print(m[0, 0, False])
    print(m[0, 0, True])