from .evolution_types import Algorithm
from .genetic_algorithms.basic import BasicGA
from .genetic_algorithms.genetic_algorithm import GA
from .genetic_algorithms.random import RandomGA
# from .genetic_algorithms.neat import NEAT


def create_ga(algorithm: Algorithm) -> GA:
    match algorithm:
        case Algorithm.RANDOM:
            return RandomGA()
        case Algorithm.BASIC:
            return BasicGA()
        case Algorithm.NEAT:
            raise Exception() # return NEAT()
