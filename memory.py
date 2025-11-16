class Memory:
    items = []
    simular_ref = []
    connection_ref = []

    def __getitem__(self, idx):
        return self.items[idx]
    
    def __setitem__(self, idx, datum):
        self.items[idx] = datum