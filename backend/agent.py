import uuid

AgentModeProperty = dict
AgentMode = dict


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
