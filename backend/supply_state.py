from enum import Enum

class SupplyState(Enum):
    OFF = 1
    IDLE = 2
    UNAVAILABLE = 3
    AVAILABLE = 4
    ACTIVE = 5
