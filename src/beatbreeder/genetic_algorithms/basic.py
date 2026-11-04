import random
from typing import cast, override

from ..evolution_types import FlatGroove, Groove
from ..util import get_random_velocity
from .genetic_algorithm import GA

### Settings
POPULATION_SIZE = 15
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
    def __init__(self):
        self.population: list[FlatGroove] = []
        for _ in range(POPULATION_SIZE):
            individual: FlatGroove = []
            for _ in range(TRACK_COUNT):
                track: list[float] = []
                for _ in range(STEPS_PER_GROOVE):
                    velocity = get_random_velocity()
                    track.append(velocity)
                individual.append(track)

            self.population.append(individual)

    @override
    def evolve(self, parents: list[int]) -> None:
        can_crossover: bool = len(parents) > 1

        new_population: list[FlatGroove] = []
        for _ in range(len(self.population)):
            if can_crossover and random.random() < CHANCE_TO_CROSSOVER:
                idx1, idx2 = 0, 0
                while idx1 == idx2:
                    idx1 = random.choice(parents)
                    idx2 = random.choice(parents)

                new_individual: FlatGroove = crossover(self.population[idx1], self.population[idx2], CROSSOVER_TYPE, CROSSOVER_BALANCE)
            else:
                idx = random.choice(parents)
                new_individual = mutate(self.population[idx], MUTATION_RATE)

            new_population.append(new_individual)

        self.population = new_population

    @override
    def grooves(self) -> list[tuple[int, Groove]]:
        formatted_output: list[tuple[int, Groove]] = []

        for i in range(len(self.population)):
            entry: tuple[int, Groove] = (i, cast(Groove, self.population[i]))
            formatted_output.append(entry)

        return formatted_output







### STATIC METHODS ###
def mutate(individual: FlatGroove, mutation_rate: float) -> FlatGroove:
    new_individual: FlatGroove = []
    for track in individual:
        new_track: list[float] = []
        for step in track:
            if random.random() < mutation_rate:
                new_track.append(get_random_velocity())
            else:
                new_track.append(step)

        new_individual.append(new_track)

    return new_individual


def crossover(individual1: FlatGroove, individual2: FlatGroove, crossover_type: str, crossover_balance: float) -> FlatGroove:
    match crossover_type:
        case "TRACK":
            return crossover_using_tracks(individual1, individual2, crossover_balance)
        case "CELL":
            return crossover_using_cells(individual1, individual2, crossover_balance)
        case _:
            raise Exception(crossover_type + " is not a valid CROSSOVER_TYPE")


def crossover_using_tracks(i1: FlatGroove, i2: FlatGroove, crossover_balance: float) -> FlatGroove:
    new_individual: FlatGroove = []
    for i in range(len(i1)):
        if random.random() < crossover_balance:
            new_individual.append(i1[i])
        else:
            new_individual.append(i2[i])

    return new_individual



def crossover_using_cells(i1: FlatGroove, i2: FlatGroove, crossover_balance: float) -> FlatGroove:
    new_individual: FlatGroove = []
    for i in range(len(i1)):
        track: list[float] = []
        for j in range(len(i1[0])):
            if random.random() < crossover_balance:
                track.append(i1[i][j])
            else:
                track.append(i2[i][j])

        new_individual.append(track)

    return new_individual
