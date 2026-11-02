from .evolution_types import Algorithm
from .genetic_algorithms.genetic_algorithm import GA
from .genetic_algorithms.neat_ga import NEAT
from .genetic_algorithms.random import RandomGA


def create_ga(algorithm: Algorithm) -> GA:
    match algorithm:
        case Algorithm.RANDOM:
            return RandomGA()
        case Algorithm.SIMPLE:
            raise NotImplementedError # TODO
        case Algorithm.NEAT:
            return NEAT()
