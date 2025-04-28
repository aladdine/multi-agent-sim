from act_state import ActState

class Ability:
    def __init__(self, name, act_type, supply_state, capacity, efficiency, start, stop, recur, every, until, err_rate):
        self.name = name
        self.act_type = act_type
        self.supply_state = supply_state
        self.capacity = capacity
        self.efficiency = efficiency
        self.start = start
        self.stop = stop
        self.recur = recur
        self.every = every
        self.until = until
        self.err_rate = err_rate
    
    def is_available(self, _from, _until):
        return False
    
    def set_period(self, start, stop):
        if start > stop: return
        self.start = start
        self.stop = stop
    
    def is_match(self, demand):
        return demand.act_type == self.act_type
    
    def get_overlap(self, demand):
        total = 0
        for t in range(self.start, self.stop):
            if t >= demand.start and t <= demand.stop:
                total += 1
        return total
    
    def attempt(self, act):
        demand = act.demand
        if not self.is_match(demand):
            act.success = False
            return ActState.START
        remaining_effort = demand.effort / self.efficiency
        if remaining_effort > self.capacity:
            act.effort = self.capacity
            demand.effort = demand.effort - (act.effort * self.efficiency)
        else:
            act.effort = remaining_effort
            demand.effort = 0
        
        act.end = act.start + act.effort
        act.success = True
        return ActState.COMPLETE