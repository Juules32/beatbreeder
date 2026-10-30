import random

from beatbreeder.genetic_algorithms.random import RandomGA

from .evolution_types import POPULATION_SIZE, Algorithm, BitmapGenotype, Generation, Genotype, Groove
from .store import store

TRACKS = 5
STEPS = 16

def generate_grooves(algorithm: Algorithm, generation: Generation | None, pids: list[int] | None) -> list[tuple[int, Groove]]:
    match algorithm:
        case Algorithm.RANDOM:
            if generation and pids:
                new_generation = RandomGA().evolve(generation, pids)
        case _:
            raise Exception("Illegal algorithm type!")
            
