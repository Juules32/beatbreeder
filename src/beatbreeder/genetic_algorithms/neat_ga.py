from typing import override

import neat
from neat.config import Config
from neat.population import Population

from ..evolution_types import POPULATION_SIZE, STEPS, TRACKS, Groove, Track
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
        for parent in parents:
            self.population.population[parent].fitness = 1

        self.population.population = self.population.reproduction.reproduce(
            self.config,
            self.population.species,
            POPULATION_SIZE,
            self.population.generation
        )

        self.population.species.speciate(
            self.config,
            self.population.population,
            self.population.generation
        )

        self.population.generation += 1

    @override
    def grooves(self) -> list[tuple[int, Groove]]:
        population: list[tuple[int, Groove]] = []
        for id, genome in self.population.population.items():
            network = neat.nn.FeedForwardNetwork.create(genome=genome, config=self.config)

            groove: Groove = []
            for instrument in range(TRACKS):
                track: Track = []
                for step in range(STEPS):
                    value: float = network.activate((instrument, step))[0]
                    track.append(value > 0.0)
                groove.append(track)
            population.append((id, groove))
        return population
