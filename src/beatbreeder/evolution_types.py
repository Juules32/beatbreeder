from enum import StrEnum

from neat.population import Population

MAX_PARENTS = 5
POPULATION_SIZE = 15

from abc import ABC, abstractmethod
from typing import override

Step = bool

Track = list[Step]

Groove = list[Track]

Generation = Population | Groove








### TODO: remove once obsolete



# NOTE: Changes to our phenotype must be reflected in the frontend
Phenotype = list[list[bool]]





class Genotype(ABC):
    @abstractmethod
    def to_phenotype(self) -> Phenotype:
        pass

class BitmapGenotype(Genotype):
    def __init__(self, bitmap: list[list[bool]]):
        self.bitmap: list[list[bool]] = bitmap

    @override
    def to_phenotype(self) -> Phenotype:
        return self.bitmap

# TODO: tilføj CPPNGenotype her



class Algorithm(StrEnum):
    RANDOM = "random"
    # TODO: tilføj "GA" og/eller "NEAT" her
