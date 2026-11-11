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
    winner: DefaultGenome = population.run(fitness_function=fitness_function, n=generations)
    print(winner.fitness)
    return population


### Fitness functions | Require parameters Callable[[list[tuple[int, DefaultGenome]], Config], None]

def random_fitness(genomes: list[tuple[int, DefaultGenome]], config: Config) -> None:  # pyright: ignore[reportUnusedParameter]
    for _, genome in genomes:
        genome.fitness = randint(0,4)

def simple_beat_fitness(genomes: list[tuple[int, DefaultGenome]], config: Config) -> None:
    # Fitness based on distance to "4 on the floor" beat
    for _, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(config=config, genome=genome)

        score = 80

        for instrument in range(TRACKS):
            for step in range(STEPS):
                value: float = network.activate((instrument, step))[0]
                hit: int = 1 if value > 0.0 else 0
                if (hit != four_on_the_floor[instrument][step]):
                    score -= 1

        genome.fitness = score

four_on_the_floor = [
    [1 if x % 2 == 0 else 0 for x in range(16)],
    [1 if (x + 2) % 4 == 0 else 0 for x in range(16)],
    [0 for _ in range(16)],
    [0 for _ in range(16)],
    [1 if x % 4 == 0 else 0 for x in range(16)],

]

### Helpers

# Simple comparison assuming standard 16*5 beat
# Groove = 5 Tracks = 16 [float]
def compare_grooves(a: list[list[int]], b: list[list[int]]) -> int:
    score = sum([len(x) for x in a])

    for i, track in enumerate(a):
        for j, step in enumerate(track):
            if step != b[i][j]:
                score -= 1

    return score
