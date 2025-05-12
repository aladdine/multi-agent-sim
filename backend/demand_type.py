from enum import Enum

"Name","API Name","Instance Memory","vCPUs","Instance Storage","Network Performance","On Demand","Linux Reserved cost","Linux Spot Minimum cost","Windows On Demand cost","Windows Reserved cost"
class DemandType(Enum):
    APP_SERVER = 1
    BATCH_PROCESSING = 2
    AI_TRAINING = 3
    AI_INFERENCE = 4
    LAMBDA = 5
