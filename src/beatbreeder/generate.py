import random

from .evolution_types import POPULATION_SIZE, Algorithm, BitmapGenotype, Genotype
from .models import Solution
from .store import store

TRACKS = 5
STEPS = 16

def generate_solutions(algorithm: Algorithm = Algorithm.RANDOM, parents: list[Genotype] | None = None) -> list[Solution]:
    solutions: list[Solution] = []
    for _ in range(POPULATION_SIZE):
        genotype = generate_genotype(algorithm, parents)
        solutions.append(Solution(id=store.add(genotype), phenotype=genotype.to_phenotype()))
    return solutions

# NOTE: This pattern is not """good programming""", but it works well enough.
# In the future, algorithms could implement an interface instead.
def generate_genotype(algorithm: Algorithm, parents: list[Genotype] | None) -> Genotype:
    match algorithm:
        case Algorithm.RANDOM:
            return random_generator(parents)
        case _:
            raise Exception("Illegal algorithm type!")

def random_generator(parents: list[Genotype] | None) -> BitmapGenotype:
    if parents:
        print(parents[0].to_phenotype())
    return BitmapGenotype([[random.random() < 0.5 for _ in range(STEPS)] for _ in range(TRACKS)])
