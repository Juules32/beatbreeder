from typing import override

import neat
from neat.config import Config
from neat.nn.feed_forward import FeedForwardNetwork
from neat.population import Population

from ..evolution_types import POPULATION_SIZE, TRACKS, Groove, Subdivision
from .genetic_algorithm import GA

MAX_DEPTH = 2

class NEATNested(GA):
    def __init__(self, config_path: str = 'nested-cppn-config'):
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

        for id in self.population.population:
            if id in parents:
                self.population.population[id].fitness = 1
            else:
                self.population.population[id].fitness = 0

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
                net_wrapper = NetworkWrapper(network, instrument)
                track: Subdivision = build_subdivisions(network=net_wrapper, max_depth=MAX_DEPTH)
                groove.append(track)
            population.append((id, groove))
        return population

class NetworkWrapper:
    def __init__(self, network: FeedForwardNetwork, instrument: int):
        self.network: FeedForwardNetwork = network
        self.instrument: int = instrument
        self.step: int = 0

    def activate(self) -> list[float]:
        result: list[float] = self.network.activate((self.instrument, self.step))
        self.step += 1
        return result

def build_subdivisions(network: NetworkWrapper, max_depth: int = 3, depth: int = 0) -> Subdivision:
    (split, velocity) = network.activate()
    if (depth == max_depth or split < 0.0):
        return [velocity] if velocity > 0.0 else [0.0]

    subdivision: Subdivision = []
    splits: int = round(split * 10.0)
    for _ in range(splits):
        sub: Subdivision = build_subdivisions(network, max_depth, depth + 1)
        subdivision.append(sub)
    if len(subdivision) == 0:
        subdivision.append([0])
    return subdivision
