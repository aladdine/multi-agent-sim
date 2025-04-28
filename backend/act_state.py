from enum import Enum

class ActState(Enum):
    PENDING = 1
    START = 2
    PARTIAL = 3 
    COMPLETE = 4
    COMMITTED = 5