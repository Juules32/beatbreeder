import random
from typing import override

from ..evolution_types import POPULATION_SIZE, TRACKS, Groove, Subdivision
from .genetic_algorithm import GA, get_random_velocity

# NOTE: These constants are here to try to contain the chaotic rhythms possible with the nested list rhythm type
BEATS = 4 # Initial subdivisions (4/4 time)
DIVISIONS = [2, 3, 4, 5] # Possible subdivisions when nesting
DIVISION_WEIGHTS = [10, 2, 6, 1] # Relatvie hance of each likelihood
NEST_CHANCE = 0.1
MAX_DEPTH = 2

class RandomGA(GA):
    def __init__(self):
        self.generation: list[Groove] = self.random_grooves()

    @staticmethod
    def random_subdivision(depth: int) -> Subdivision:
        parts = random.choices(DIVISIONS, DIVISION_WEIGHTS)[0]
        if depth < MAX_DEPTH and random.random() < NEST_CHANCE:
            return [RandomGA.random_subdivision(depth + 1) for _ in range(parts)]
        return [get_random_velocity() for _ in range(parts)]

    @staticmethod
    def random_grooves() -> list[Groove]:
        return [[[RandomGA.random_subdivision(1) for _ in range(BEATS)] for _ in range(TRACKS)] for _ in range(POPULATION_SIZE)]

    @override
    def evolve(self, parents: list[int]) -> None:
        self.generation = self.random_grooves()

    @override
    def grooves(self) -> list[tuple[int, Groove]]:
        return list(enumerate(self.generation))
