from enum import Enum

# Activity types that demand is requesting.
class ActType(Enum):
    # figure out FLOPS
    # include efficiency factor: 60%
    ML_TRAINING = 1
    # estimate based on number of tokens
    ML_INFERENCE = 2
    LAMBDA = 3 
    WEB_API = 4
    CRON_JOB = 5
    STREAMING = 6
    STORAGE = 7
