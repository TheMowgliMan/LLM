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
            return len(self.connection_ref[idx]) - 1
        else:
            self.similar_ref[idx].append([ref, count])
            return len(self.similar_ref[idx]) - 1

    def get_all_refs_at_item(self, idx, type=False):
        if type: # connection ref
            return tuple(self.connection_ref[idx])
        else:
            return tuple(self.similar_ref[idx])
        
    def get_ref(self, idx_item, idx_ref, type=False):
        if type: # connection ref
            return tuple(self.connection_ref[idx_item][idx_ref])
        else:
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

    def set_count(self, idx_item, idx_ref, count, type=False):
        if type:
            self.connection_ref[idx_item][idx_ref] = [self.connection_ref[idx_item][idx_ref][0], count]
        else:
            self.similar_ref[idx_item][idx_ref] = [self.similar_ref[idx_item][idx_ref][0], count]

    def increment_count(self, idx_item, idx_ref, count, type=False):
        if type:
            self.connection_ref[idx_item][idx_ref][1] = count + self.connection_ref[idx_item][idx_ref][1]
        else:
            self.similar_ref[idx_item][idx_ref][1] = count + self.similar_ref[idx_item][idx_ref][1]

    def follow_ref(self, idx_item, idx_ref, type=False):
        if type:
            return self.items[self.connection_ref[idx_item][idx_ref][0]]
        else:
            return self.items[self.similar_ref[idx_item][idx_ref][0]]
        
    def find_ref(self, idx_item, item, type=False):
        if len(self.items) != len(self.similar_ref) != len(self.connection_ref):
            print("error!")

        idx = None
        if not item in self.items:
            self.append(item)
            idx = self.__len__() - 1
        else:
            idx = self.items.index(item)
        if type:
            i = 0
            for ref in self.connection_ref[idx_item]:
                if ref[0] == idx:
                    self.increment_count(idx_item, i, 1, type=True)
                    return None
                i += 1
            return self.add_ref(idx_item, idx, type=True, count=1)
        else:
            i = 0
            for ref in self.similar_ref[idx_item]:
                if ref[0] == idx:
                    self.increment_count(idx_item, i, 1, type=False)
                    return None
                i += 1
            return self.add_ref(idx_item, idx, type=False, count=1)
        
    def index(self, item):
        return self.items.index(item)
    
    def import_str(self, stri):
        words = stri.split()
        for i in range(len(words)):
            if i == 0:
                self.append(words[i].lower())
            elif i == 1:
                if words[i - 1].lower() in self.items:
                    self.find_ref(self.index(words[i - 1].lower()), words[i].lower())
                else:
                    self.append(words[i].lower())
            else:
                found = False
                if words[i - 1].lower() in self.items:
                    self.find_ref(self.index(words[i - 1].lower()), words[i].lower())
                    found = True
                if words[i - 2].lower() in self.items:
                    self.find_ref(self.index(words[i - 2].lower()), words[i].lower(), type=True)
                    found = True
                if not found:
                    self.append(words[i].lower())


if __name__ == "__main__": # Unit tests
    m = Memory()
    m.append("buh 1")
    second = m.append("buh 2")
    third = m.append("buh 3")
    cats = m.add_ref(second, 1, count=2)
    print(cats)
    mice = m.add_ref(second, 2, count=14)
    zyzzy = m.add_ref(third, 1, type=True)

    for item in m:
        print(item)

    print("----------")

    for item in m.get_all_refs_at_item(second):
        print(item)

    print("----------")

    print(m.get_ref(second, cats))

    m.set_ref(1, mice, 1)
    m.set_ref(1, cats, 0, count=3)
    m.set_count(third, zyzzy, 3, type=True)

    print("----------")

    for item in m:
        print(item)

    m.increment_count(second, cats, 100)

    print("----------")

    for item in m:
        print(item)
    print(m.follow_ref(second, cats))

    print("----------")
    m.find_ref(second, "buh 1")
    m.find_ref(second, "buh 1")
    m.find_ref(second, "buh 2")
    m.find_ref(second, "buh 3")
    m.find_ref(second, "bruh")
    for item in m:
        print(item)