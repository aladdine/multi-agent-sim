import uuid
import pandas as pd


AgentModeProperty = dict
AgentMode = dict

class ClusterTable:
    def __init__(self):
        self.clusters = {}
    
    def get_all_clusters(self):
        return self.clusters

    def get_cluster(self, id):
        return self.clusters.get(id)
    
    def add_cluster(self, cluster):
        self.clusters[cluster.getId()] = cluster
    
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
    
    def getId(self) -> str:
        return self.uuid


class Agent:
    
    def __init__(self):
        self.uuid = uuid.uuid5()
        self.mode = None
        self.signal = None

    def getId(self) -> str:
        return self.uuid

    def getMode(self):
        return self.mode

    def setAgentMode(self, mode):
        self.mode = mode

    def getSignal(self):
        return self.signal
    
    def setSignal(self, signal):
        self.signal = signal
