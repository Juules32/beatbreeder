from enum import StrEnum

MAX_PARENTS = 5
POPULATION_SIZE = 15
TRACKS = 5
STEPS = 16

type Subdivision = list[Subdivision] | list[float]
type Groove = list[Subdivision]
type FlatGroove = list[list[float]]

class Algorithm(StrEnum):
    RANDOM = "random"
    BASIC = "basic"
    NEAT = "neat"
    NEATNESTED = "neat nested"
