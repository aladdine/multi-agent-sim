from act_state import ActState

class Act:
    def __init__(self, agent, supply, demand, start, end, effort, success, act_state):
        self.agent = agent
        self.supply = supply
        self.demand = demand
        self.start = start
        self.end = end
        self.effort = effort
        self.success = success
        self.act_state = act_state
    
    def get_set(self, time_start, agent, supply, demand):
        self.agent = agent
        self.supply = supply
        self.demand = demand
        self.start = time_start
        self.act_state = ActState.START
    
    def attempt(self):
        self.state = self.supply.attempt(self)

    def rollback(self):
        pass

    def wrap_up(self, time_stop, effort, success):
        self.end = time_stop
        self.effort = effort
        self.success = success
    