from enum import Enum

# State of the activity on demand.
class ActState(Enum):
    PENDING = 1
    START = 2
    PARTIAL = 3 
    COMPLETE = 4
    COMMITTED = 5