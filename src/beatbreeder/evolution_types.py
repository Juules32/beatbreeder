from enum import StrEnum

MAX_PARENTS = 5
POPULATION_SIZE = 15
TRACKS = 5
STEPS = 16

Step = bool
Track = list[Step]
Groove = list[Track]

class Algorithm(StrEnum):
    RANDOM = "random"
    SIMPLE = "simple"
    NEAT = "neat"
