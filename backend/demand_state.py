from enum import Enum

class DemandState(Enum):
    INACTIVE = 1
    PENDING = 2
    STARTING = 3
    ACTIVE = 4
    COMPLETE = 5
    IGNORED = 6