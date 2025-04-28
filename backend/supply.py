class Supply:
    def __init__(self, name, capacity, act_type, efficiency, start, stop, recur, every, until):
        self.name = name
        self.capacity = capacity
        self.act_type = act_type
        self.efficiency = efficiency
        self.start = start
        self.stop = stop
        self.recur = recur
        self.every = every
        self.until = until
    
    def is_match(self, demand):
        pass

    def attempt(self, act):
        pass
