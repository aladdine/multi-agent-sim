import uuid
import pandas as pd


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
    def __init__(self, name):
        self.uuid = uuid.uuid4().__str__()
        self.name = name
        self.mode = None
        self.signal = None
        self.supplies = None
        self.demands = None
        self.agent_time = agent_time

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
    
    def loop(self):
        pass

    def step(self):
        pass
    
    def reset(self):
        pass

    def observe(self):
        pass

    def select(self):
        pass

    def act(self):
        pass

    def complete(self):
        pass
    
