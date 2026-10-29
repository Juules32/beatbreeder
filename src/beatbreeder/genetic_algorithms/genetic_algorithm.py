from abc import ABC, abstractmethod

from ..evolution_types import Groove
from ..generations.generation import Generation


# Genetic Algorithm abstract class
class GA(ABC): 
    @abstractmethod
    def init_generation() -> Generation:
        ...

    @abstractmethod
    def evolve(self, generation: Generation, parents: list[int]) -> Generation:
        ...

    @abstractmethod
    def make_grooves(self, generation: Generation) -> list[tuple[int, Groove]]:
        ...
