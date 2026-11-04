import random
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

def get_random_velocity() -> float:
    ACTIVE_CHANCE = 0.3
    MINIMUM_VELOCITY = 0.3
    MAXIMUM_VELOCITY = 1.0

    is_active = random.random() < ACTIVE_CHANCE
    if is_active:
        velocity = random.random()
        return MINIMUM_VELOCITY + velocity * (MAXIMUM_VELOCITY - MINIMUM_VELOCITY)
    else:
        return 0.0
