from typing_extensions import override

from ..generations.generation import Generation
from ..generations.basic import BasicGeneration
from ..evolution_types import Groove, Track
from .genetic_algorithm import GA

import random


### Settings
POPULATION_SIZE = 5
TRACK_COUNT = 5
STEPS_PER_GROOVE = 16

# INITIALIZATION SETTINGS
CHANCE_TO_ADD_BEAT = 0.25  # between 0 and 1

# EVOLUTION SETTINGS
MUTATION_RATE = 0.15
CHANCE_TO_CROSSOVER = 0.5
CROSSOVER_BALANCE = 0.5
CROSSOVER_TYPE = "TRACK"  # Either "TRACK" or "CELL"
### No more settings


class BasicGA(GA):
    @override
    def init_generation(self) -> Generation:
        population: list[Groove] = []
        for _ in range(STEPS_PER_GROOVE):
            individual: Groove = []
            for _ in range(TRACK_COUNT):
                track: Track = []
                for _ in range(STEPS_PER_GROOVE):
                    if random.random() < CHANCE_TO_ADD_BEAT:
                        track.append(True)
                    else:
                        track.append(False)
                individual.append(track)

            population.append(individual)

        new_generation = BasicGeneration(population)
        return new_generation

    @override
    def evolve(self, generation: Generation, parents: list[int]) -> Generation:
        population: list[Groove] = generation.get_population()

        can_crossover: bool = len(parents) > 1

        new_population: list[Groove] = []
        for _ in range(len(population)):
            if can_crossover and random.random() < CHANCE_TO_CROSSOVER:
                idx1, idx2 = 0, 0
                while idx1 == idx2:
                    idx1 = random.choice(parents)
                    idx2 = random.choice(parents)

                new_individual: Groove = crossover(population[idx1], population[idx2], CROSSOVER_TYPE, CROSSOVER_BALANCE)
            else:
                idx = random.choice(parents)
                new_individual: Groove = mutate(population[idx], MUTATION_RATE)

            new_population.append(new_individual)

        new_generation = BasicGeneration(new_population)
        return new_generation



### STATIC METHODS ###
def mutate(individual: Groove, mutation_rate: float) -> Groove:
    new_individual: Groove = []
    for track in individual:
        new_track: Track = []
        for step in track:
            if random.random() < mutation_rate:
                new_track.append(not step)
            else:
                new_track.append(step)

        new_individual.append(new_track)

    return new_individual


def crossover(individual1: Groove, individual2: Groove, crossover_type: str, crossover_balance: float) -> Groove:
    match crossover_type:
        case "TRACK":
            return crossover_using_tracks(individual1, individual2, crossover_balance)
        case "CELL":
            return crossover_using_cells(individual1, individual2, crossover_balance)
        case _:
            raise Exception(crossover_type + " is not a valid CROSSOVER_TYPE")


def crossover_using_tracks(i1: Groove, i2: Groove, crossover_balance: float) -> Groove:
    new_individual: Groove = []
    for i in range(len(i1)):
        if random.random() < crossover_balance:
            new_individual.append(i1[i])
        else:
            new_individual.append(i2[i])

    return new_individual


def crossover_using_cells(i1: Groove, i2: Groove, crossover_balance: float) -> Groove:
    new_individual: Groove = []
    for i in range(len(i1)):
        track: Track = []
        for j in range(len(i1[0])):
            if random.random() < crossover_balance:
                track.append(i1[i][j])
            else:
                track.append(i2[i][j])

        new_individual.append(track)

    return new_individual
