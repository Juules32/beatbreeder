from abc import ABC, abstractmethod

from ..evolution_types import Generation, Groove


# Genetic Algorithm abstract class
class GA[T: Generation](ABC):
    @abstractmethod
    def init_generation() -> T:
        ...

    @abstractmethod
    def evolve(self, generation: T, parents: list[int]) -> T:
        ...

    @abstractmethod
    def make_grooves(self, generation: T) -> list[tuple[int, Groove]]:
        ...
