import uuid
import pandas as pd
import streamlit as st

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
    "duration",
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

    def __init__(self, name, hardware_type, start_time, delayable, num_jobs, repeat_every, duration, power_consumption, heat_decipation):
        self.id = uuid.uuid4().__str__()
        self.name = name
        self.hardware_type = hardware_type
        self.start_time = start_time
        self.delayable = delayable
        self.num_jobs = num_jobs # TODO: convert this to auto-scaling
        self.repeat_every = repeat_every
        self.duration = duration # TODO: convert this to FLOPS
        self.power_consumption = power_consumption
        self.heat_decipation = heat_decipation
        self.act_type = None
        self.state = None
        
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
    
    def getStartTime(self):
        return self.start_time
    
    def setStartTime(self, start_time):
        self.start_time = start_time

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
    
    def getDuration(self):
        return self.duration

    def setDuration(self, duration):
        self.duration = duration
    
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
