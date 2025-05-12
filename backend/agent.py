import uuid
import pandas as pd
import random
from .agent_mode import AgentMode
from .demand_state import DemandState
from .act import Act
from .act_state import ActState


class ClusterTable:
    def __init__(self):
        self.clusters = {}
    
    def get_all_clusters(self):
        return self.clusters

    def get_cluster(self, id):
        return self.clusters.get(id)
    
    def add_cluster(self, cluster):
        self.clusters[cluster.get_id()] = cluster
    
    def remove_cluster(self, cluster_id):
        del self.clusters[cluster_id] 
    
    def get_df(self):
        data = [c.__dict__ for c in self.clusters.values()]
        return pd.DataFrame.from_records(data)


class Cluster:
    def __init__(self, name, hardware_type, size, failure_rate):
        self.uuid = uuid.uuid4().__str__()
        self.name = name
        self.hardware_type = hardware_type
        self.size = size
        self.failure_rate = failure_rate
    
    def get_id(self):
        return self.uuid


class Agent:
    def __init__(self, name, supplies, demands, signals, mode, place, agent_time):
        self.uuid = uuid.uuid4().__str__()
        self.name = name
        self.supplies = supplies
        self.demands = demands
        self.acts = []
        self.signals = signals
        self.mode = mode
        self.place = place
        self.agent_time = agent_time
        self.selected_demand = None
        self.selected_supply = None
        self.in_process_act = None

        self.random_select = False
        self.random_act = False
        self.random_observe = False
        self.pending_limit = 1 # demands that can be observed and pending simultaneously
        self.active_limit = 3 # demands that can be active simultaneously      
        self.wait_duration = 300
        self.observation_duration = 300

        self.effort_work_cumulative = 0
        self.effort_com_cumulative = 0


    def get_id(self):
        return self.uuid

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        self.mode = mode

    def get_signal(self):
        return self.signal
    
    def set_signal(self, signal):
        self.signal = signal
    
    def get_supplies(self):
        return self.supplies
    
    def set_supplies(self, supplies):
        self.supplies = supplies
    
    def get_demands(self):
        return self.demands
    
    def set_demands(self, demands):
        self.demands = demands
    
    def get_agent_time(self):
        return self.agent_time
    
    def set_agent_time(self, agent_time):
        self.agent_time = agent_time
    
    def step(self):
        if self.mode == AgentMode.IDLE:
            self.mode = AgentMode.OBSERVING
        elif self.mode == AgentMode.WAITING:
            self.mode = None
        elif self.mode == AgentMode.OBSERVING:
            self.mode = self.observe()
        elif self.mode == AgentMode.SELECTING:
            self.mode = self.select()
        elif self.mode == AgentMode.ACTING:
            self.mode = self.act()
        elif self.mode == AgentMode.COMPLETING:
            self.mode = self.complete()
        elif self.mode == AgentMode.TERMINATING:
            _ = self.terminate()
        elif self.mode == AgentMode.PAUSED:
            return 
        
    def reset(self):
        self.agent_time = 0
        self.demands = None
        self.acts = None

        self.selected_demand = None
        self.selected_supply = None
        self.in_process_act = None

        self.reset_metrics()

        self.mode = AgentMode.IDLE

    def observe(self):
        size = len(self.signals)
        offset = self.random_observe if self.get_random_demand(self.signals, DemandState.INACTIVE) else 0
        pending_count = self.count_demands(self.demands, DemandState.PENDING)
        for i in range(size):
            if pending_count >= self.pending_limit:
                return
            d = self.signals[(i+offset)%size]
            if (d not in self.demands and d.state==DemandState.INACTIVE):
                self.demands.append(d)
                d.state = DemandState.PENDING
                pending_count += 1

        if self.count_demands(self.demands, [DemandState.PENDING, DemandState.ACTIVE]) == 0:
            p = self.place
            for c in self.get_connects_to(p):    
                if self.has_remaining_effort(c):
                    self.move_to(c)
                    self.agent_time = self.agent_time + 1
                    return AgentMode.OBSERVING
                
            self.agent_time = self.agent_time + self.wait_duration
            return AgentMode.WAITING
        self.agent_time = self.active_limit + self.observation_duration
        return AgentMode.SELECTING

    def get_random_demand(self, demands, demand_state):
        # TODO: fix this to get random demand.
        size = self.count_demands(demands, demand_state)
        offset = round(random.random(),0) * size
        return demands[offset]
    
    def count_demands(self, demand, demand_states):
        count = 0
        for d in demand:
            if d.state in demand_states:
                count += 1
        return count
    
    def move_to(self, p):
        self.place = p
    
    def select(self):
        curr_agent_mode = None
        offset = 0
        self.selected_demand = None
        size = self.count_demands(self.demands, DemandState.ACTIVE)
        if size:
            if self.random_act == True:
                offset = self.get_random_demand(self.demands, DemandState.ACTIVE)
            for n in range(len(self.demands)):
                d = self.demands[(n+offset) % len(self.demands)]
                if d.state != DemandState.ACTIVE:
                    continue
                s = self.match(d)
                if s:
                    self.selected_demand = d
                    self.selected_supply = s
                    return AgentMode.ACTING
                else:
                    d.state = DemandState.IGNORED
        
        curr_agent_mode = AgentMode.OBSERVING
        offset = 0
        size = self.count_demands(self.demands, DemandState.PENDING)
        if size:
            if self.random_select:
                offset = self.get_random_demand(self.demands, DemandState.PENDING)
            for n in range(len(self.demands)):
                if self.count_demands(self.demands, DemandState.ACTIVE) >= self.active_limit:
                    break
                d = self.demands[(n+offset) % len(self.demands)]
                if d.state != DemandState.PENDING:
                    continue

                s = self.match(d)
                if s:
                    self.selected_demand = d
                    self.selected_supply = s
                    d.state = DemandState.ACTIVE
                    curr_agent_mode = AgentMode.ACTING
                else:
                    d.state = DemandState.IGNORED
        return curr_agent_mode

    def match(self, d):
        for s in self.supplies:
            if s.is_match(d):
                return s
        return None

    def do_nothing(self):
        self.agent_time = self.agent_time + 1
        return AgentMode.OBSERVING
    
    def act(self):
        a = Act()
        a.get_set(self.agent_time, self, self.selected_supply, self.selected_demand)
        self.in_process_act = a
        a.agent = self
        self.acts.append(a)
        a.attempt()
        self.agent_time = a.end
        if self.selected_demand.effort == 0:
            return AgentMode.COMPLETING
        else:
            return AgentMode.ACTING

    def complete(self):
        self.selected_demand.state = DemandState.COMPLETE
        self.selected_demand = None
        self.selected_supply = None
        self.in_process_act = None
        return AgentMode.OBSERVING
    
    def commit(self, global_time):
        for a in self.acts:
            if a.state == ActState.COMPLETE:
                if global_time >= a.end:
                    a.state = ActState.COMMITTED
    
    def terminate(self):
        return None

    def loop(self):
        pass
    
    def reset_metrics(self):
        self.effort_work_cumulative = 0
        self.effort_com_cumulative = 0