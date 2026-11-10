from collections.abc import Callable
from random import randint

import neat
from neat.config import Config
from neat.genome import DefaultGenome
from neat.population import Population

from ..evolution_types import STEPS, TRACKS, Groove, Subdivision

### Evolve functions

def evolve(config: Config, fitness_function: Callable[[list[tuple[int, DefaultGenome]], Config], None], generations: int = 300) -> Population:
    population = neat.Population(config)
    _: DefaultGenome = population.run(fitness_function=fitness_function, n=generations)
    return population


### Fitness functions | Require parameters Callable[[list[tuple[int, DefaultGenome]], Config], None]

def random_fitness(genomes: list[tuple[int, DefaultGenome]], config: Config) -> None:  # pyright: ignore[reportUnusedParameter]
    for _, genome in genomes:
        genome.fitness = randint(0,4)

def beat_fitness(genomes: list[tuple[int, DefaultGenome]], config: Config) -> None:
    for _, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(config=config, genome=genome)

        groove: Groove = []
        for instrument in range(TRACKS):
            track: Subdivision = []
            for step in range(STEPS):
                value: float = network.activate((instrument, step))[0]
                velocity: list[float] = [value] if value > 0.0 else [0.0]
                track.append(velocity)
            groove.append(track)


### Helpers

# Simple comparison assuming standard 16*5 beat
# Groove = 5 Tracks = 16 [float]
def compare_grooves(a: Groove, b: Groove) -> float:
    ...
