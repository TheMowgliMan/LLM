class Memory:
    items = []

    # Store references to items that are different in form but similar in meaning
    similar_ref = [] # Format: [[[idx1, count1], [idx2, count2], [...] [idxX, countX]], [[idx1, count1], [idx2, count2], [...] [idxX, countX]]]
    # Store references to items that are connected to this one
    connection_ref = [] # Format: [[[idx1, count1], [idx2, count2], [...] [idxX, countX]], [[idx1, count1], [idx2, count2], [...] [idxX, countX]]]

    def __getitem__(self, foo):
        return self.items[foo]
    
    def __setitem__(self, foo, datum):
        self.items[foo] = datum

    def __len__(self):
        return len(self.items)
    
    def __iter__(self):
        for i in range(len(self.items)):
            yield tuple((self.items[i], self.similar_ref[i], self.connection_ref[i]))
        
    def append(self, datum):
        self.items.append(datum)
        self.similar_ref.append([])
        self.connection_ref.append([])
        return len(self.items) - 1

    def add_ref(self, idx, ref, type=False, count=None):
        if type: # connection ref
            self.connection_ref[idx].append([ref, count])
            return len(self.connection_ref) - 1
        else:
            self.similar_ref[idx].append([ref, count])
            return len(self.similar_ref) - 1

    def get_all_refs_at_item(self, idx, type=False):
        if type: # connection ref
            return tuple(self.connection_ref[idx])
        else:
            return tuple(self.similar_ref[idx])
        
    def get_ref(self, idx_item, idx_ref, type=False):
        if type: # connection ref
            return tuple(self.connection_ref[idx_item][idx_ref])
        else:
            print(idx_ref)
            return tuple(self.similar_ref[idx_item][idx_ref])
        
    def set_ref(self, idx_item, idx_ref, ref, type=False, count=None):
        if type: # Connection ref
            if count == None:
                self.connection_ref[idx_item][idx_ref] = [ref, self.connection_ref[idx_item][idx_ref][1]]
            else:
                self.connection_ref[idx_item][idx_ref] = [ref, count]
        else:
            if count == None:
                self.similar_ref[idx_item][idx_ref] = [ref, self.similar_ref[idx_item][idx_ref][1]]
            else:
                self.similar_ref[idx_item][idx_ref] = [ref, count]


if __name__ == "__main__":
    m = Memory()
    m.append("buh 1")
    second = m.append("buh 2")
    m.append("buh 3")
    cats = m.add_ref(second, "cat", count=2)
    print(cats)
    # mice = m.add_ref(second, "mouse", count=14)


    for item in m:
        print(item)

    for item in m.get_all_refs_at_item(second):
        print(item)

    print(cats)
    # print(mice)
    print(m.get_ref(second, cats))

    # m.set_ref(1, mice, "dead mouse")
    m.set_ref(1, cats, "cat", count=3)

    for item in m:
        print(item)