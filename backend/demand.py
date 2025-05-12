import uuid
import pandas as pd
import streamlit as st
from .demand_state import DemandState
from .act_type import ActType


COLUMNS = [
    "name",
    "hardware_type",
    "start_time",
    "delayable",
    "num_jobs",
    "repeat_every",
    "repeat_until",
    "effort",
    "power_consumption",
    "heat_decipation"
]

class DemandTable:
    def __init__(self):
        self.demands = {}
        self.sorted_demands = []
    
    def get_all_demand(self):
        return self.demands

    def get_demand(self, id):
        return self.demands.get(id)
    
    def add_demand(self, demand):
        self.demands[demand.id] = demand
    
    def remove_demand(self, demand_id):
        del self.demands[demand_id] 
    
    def get_df(self):
        data = [d.__dict__ for d in self.demands.values()]
        return pd.DataFrame.from_records(data)

    def get_chart(self):
        steps = 300
        columns = []
        data = [None] * steps
        demand_data = [d.__dict__ for d in self.demands.values()]
        for i in range(steps):
            data[i] = []
        
        for dd in demand_data:
            columns.append(dd.get("name"))
            num_of_instances = dd.get("num_of_instances")
            repeat_every = dd.get("repeat_every")
            repeat_until = dd.get("repeat_until")
            start_time = dd.get("start_time")
            duration = dd.get("duration")
            curr_duration = duration
            for i in range(repeat_until):
                
                if i < start_time:
                    data[i].append(0)
                    break
                if i == start_time:
                    data[i].append(num_of_instances)
                    continue
                if repeat_every == 0:
                    break
                if (i-start_time) % repeat_every == 0:
                    curr_duration = duration
                    data[i].append(num_of_instances)
                else:
                    data[i].append(0)

                if curr_duration > 1:
                    data[i][-1] = data[i][-1] + num_of_instances
                    curr_duration = curr_duration - 1

        print("data", data)
        return pd.DataFrame(data, columns=columns)
        

class Demand:

    def __init__(self, name, workload_type, start_time, num_of_instances, 
                 repeat_every, repeat_until, duration, memory_gib, vcpus):

        self.id = uuid.uuid4().__str__()
        self.name = name
        self.workload_type = workload_type
        self.start_time = start_time
        self.num_of_instances = num_of_instances
        self.repeat_every = repeat_every
        self.repeat_until = repeat_until
        self.duration = duration
        self.memory_gib = memory_gib
        self.vcpus = vcpus
        self.act_type = ActType.PROCESS
        self.state = DemandState.INACTIVE

    
    def is_active(self, now):
        if self.repeat_every:
            return now >= self.start_time and now <= self.repeat_until
        else:
            return now >= self.start_time and now <= (self.start_time + self.duration)
    
    def set_period(self, start, end):
        self.start_time = start
        self.repeat_until = end
    
    def reset(self):
        self.start_time = 0
        self.state = DemandState.INACTIVE
