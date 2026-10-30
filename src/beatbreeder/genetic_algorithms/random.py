from random import random
from typing import override

from ..evolution_types import POPULATION_SIZE, STEPS, TRACKS, Groove
from .genetic_algorithm import GA


class RandomGA(GA):
    def __init__(self):
        self.generation: list[Groove] = self.random_generation()

    @staticmethod
    def random_groove() -> Groove:
        return [[random() < 0.5 for _ in range(STEPS)] for _ in range(TRACKS)]

    @staticmethod
    def random_generation() -> list[Groove]:
        return [RandomGA.random_groove() for _ in range(POPULATION_SIZE)]

    @override
    def evolve(self, parents: list[int]) -> None:
        self.generation = self.random_generation()

    @override
    def grooves(self) -> list[tuple[int, Groove]]:
        return list(enumerate(self.generation))
