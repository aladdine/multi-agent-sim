import uuid
import act_type, act_state

class Supply:
    def __init__(self, name, supply_state, capacity, efficiency, start, stop, recur, every, until, err_rate):
        self.id = uuid.uuid4().__str__()
        self.name = name
        self.supply_state = supply_state
        self.capacity = capacity
        self.efficiency = efficiency

        self.act_type = act_type.ActType.WEB_API
        
        self.start = start
        self.stop = stop
        self.recur = recur
        self.every = every
        self.until = until

        self.err_rate = err_rate
    
    def recurrence(self, every, until):
        self.recur = True
        self.every = every
        self.until = until
    
    def is_match(self, demand):
        return demand.act_type == self.act_type
    
    def get_overlap(self, demand):
        total = 0
        for i in range(self.start, self.until):
            if i >= demand.start_time and i <= demand.repeat_until:
                total += 1
        return total
    

    def attempt(self, act):
        demand = act.demand
        if not self.is_match(demand):
            act.success = False
            return act_state.ActState.START
        act_effort_remaining = demand.effort / self.efficiency
        if act_effort_remaining > self.capacity:
            act.effort = self.capacity
            demand.effort = act.effort * self.efficiency
        else:
            act.effort = act_effort_remaining
            demand.effort = 0
        
        act.end = act.start + act.effort
        act.success = True
        return act_state.ActState.COMPLETE
