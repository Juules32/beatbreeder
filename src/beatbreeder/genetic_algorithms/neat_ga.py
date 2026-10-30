from typing import override

import neat
from neat.config import Config
from neat.population import Population

from ..evolution_types import Groove
from .genetic_algorithm import GA


class NEAT(GA[Population]):
    def __init__(self, config_path: str = 'cppn-config'):
        self.config: Config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path
        )

    @override
    def init_generation(self) -> Population:
        population = neat.Population(self.config)
        return population

    @override
    def evolve(self, generation: Population, parents: list[int]) -> Population:
        population: Population = generation

        # TODO

        return population

    @override
    def make_grooves(self, generation: Population) -> list[tuple[int, Groove]]:
        # TODO
        ...
