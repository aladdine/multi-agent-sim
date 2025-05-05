import uuid
import pandas as pd
import streamlit as st
import demand_state
import act_type
import demand_state

WORK_TYPE = ["WORK"]
HARDWARE_TYPES = ["CPU 1core", "CPU 16core", "GPU", "DPU", "ASIC"]

DEFAULTS = {
    "TYPE": WORK_TYPE[0],
    "HARDWARE_TYPES": HARDWARE_TYPES[0],
    "NUMBER_OF_JOBS": 1,
    "PRIORITY": 0
}

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
    
    def get_all_demand(self):
        return self.demands

    def get_demand(self, id):
        return self.demands.get(id)
    
    def add_demand(self, demand):
        self.demands[demand.getId()] = demand
        print("self", self.demands)
    
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
            num_jobs = dd.get("num_jobs")
            repeat_every = dd.get("repeat_every")
            repeat_until = dd.get("repeat_until")
            start_time = dd.get("start_time")
            for i in range(steps):
                if i < start_time:
                    data[i].append(0)
                elif repeat_every and (i-start_time) % repeat_every == 0:
                    data[i].append(num_jobs)
                else:
                    data[i].append(0)



                    
        return pd.DataFrame(data, columns=columns)
        

class Demand:

    def __init__(self, name, hardware_type, start_time, delayable, num_jobs, repeat_every, repeat_until, effort, power_consumption, heat_decipation):
        self.id = uuid.uuid4().__str__()
        self.name = name
        self.hardware_type = hardware_type
        self.start_time = start_time
        self.delayable = delayable
        self.num_jobs = num_jobs # TODO: convert this to auto-scaling
        self.repeat_every = repeat_every
        self.repeat_until = repeat_until
        self.effort = effort # TODO: convert this to FLOPS
        self.power_consumption = power_consumption
        self.heat_decipation = heat_decipation
        self.act_type = act_type.ActType.WEB_API
        self.state = demand_state.DemandState.INACTIVE
        
        # self.cores = 8 
        # for gpus SMs: streaming multi-processor.
        self.memory_mb = 40
        self.storage_mb = 500
        self.replicas = 2

    
    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name
    
    def getHardwareType(self):
        return self.hardware_type
    
    def setHardwareType(self, hardware_type):
        self.hardware_type = hardware_type
    
    def getStart(self):
        return self.start
    
    def setStart(self, start):
        self.start = start
    
    def getStop(self):
        return self.stop
    
    def setStop(self, stop):
        self.stop = stop

    def getDelayable(self):
        return self.priority

    def setDelayable(self, delayable):
        self.priority = delayable
    
    def getNumJobs(self):
        return self.num_jobs

    def setNumJobs(self, num_jobs):
        self.num_jobs = num_jobs

    def getRepeatEvery(self):
        return self.repeat_every

    def setRepeatEvery(self, repeat_every):
        self.repeat_every = repeat_every
    
    def getRepeatUntil(self):
        return self.repeat_until

    def setRepeatUntil(self, repeat_until):
        self.repeat_until = repeat_until
    
    def getEffort(self):
        return self.effort

    def setEffort(self, effort):
        self.effort = effort
    
    def getPowerConsumption(self):
        return self.power_consumption

    def setPowerConsumption(self, power_consumption):
        self.power_consumption = power_consumption
    
    def getPowerConsumption(self):
        return self.power_consumption

    def setPowerConsumption(self, power_consumption):
        self.power_consumption = power_consumption
    
    def getHeatDecipation(self):
            return self.heat_decipation

    def setHeatDecipation(self, heat_decipation):
        self.heat_decipation = heat_decipation

    def getActType(self):
        return self.act_type

    def setActType(self, act_type):
        self.act_type = act_type
    
    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state
    
    def isActive(self, now):
        if self.repeat_every:
            return now >= self.start_time and now <= self.repeat_until
        else:
            return now >= self.start_time and now <= (self.start_time + self.effort)
    
    def setPriod(self, start, end):
        self.start_time = start
        self.repeat_until = end
    
    def reset(self):
        self.start_time = 0
        self.state = demand_state.DemandState.INACTIVE
