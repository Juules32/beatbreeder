from random import random
from typing import override

from ..evolution_types import POPULATION_SIZE, Groove
from ..generate import STEPS, TRACKS
from .genetic_algorithm import GA


class RandomGA(GA[list[Groove]]):
    def random_generator(self) -> Groove:
        return [[random() < 0.5 for _ in range(STEPS)] for _ in range(TRACKS)]

    @override
    def init_generation(self) -> list[Groove]:
        return [self.random_generator() for _ in range(POPULATION_SIZE)]

    @override
    def evolve(self, generation: list[Groove], parents: list[int]) -> list[Groove]:
        return self.init_generation()

    @override
    def make_grooves(self, generation: list[Groove]) -> list[tuple[int, Groove]]:
        return [(i, generation[i]) for i in range(len(generation))]
