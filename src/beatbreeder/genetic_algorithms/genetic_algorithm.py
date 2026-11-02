from abc import ABC, abstractmethod

from ..evolution_types import Groove


# NOTE: Each instance owns a current generation
class GA(ABC):
    @abstractmethod
    def evolve(self, parents: list[int]) -> None:
        ...

    @abstractmethod
    def grooves(self) -> list[tuple[int, Groove]]:
        ...
