from typing import override

import neat
from neat.config import Config
from neat.population import Population

from ..evolution_types import Groove
from .genetic_algorithm import GA


class NEAT(GA):
    def __init__(self, config_path: str = 'cppn-config'):
        self.config: Config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path
        )
        self.population: Population = neat.Population(self.config)

    @override
    def evolve(self, parents: list[int]) -> None:
        population = neat.Population(self.config)

        # TODO
        raise NotImplementedError

    @override
    def grooves(self) -> list[tuple[int, Groove]]:
        population: Population = self.population

        # TODO
        raise NotImplementedError
