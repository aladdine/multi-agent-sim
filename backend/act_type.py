from enum import Enum

# Activity types that demand is requesting.
class ActType(Enum):
    # figure out FLOPS
    # include efficiency factor: 60%
    # estimate based on number of tokens
    PROCESS = 1
    RESCHEDULE = 2
