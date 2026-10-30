from .generation import Generation
from ..evolution_types import Groove


class BasicGeneration(Generation):
    def __init__(self, population: list[Groove]) -> None:
        self.population: list[Groove] = population

    def get_population(self) -> list[Groove]:
        return self.population
