from .evolution_types import Algorithm
from .genetic_algorithms.basic import BasicGA
from .genetic_algorithms.genetic_algorithm import GA
from .genetic_algorithms.neat_ga import NEAT
from .genetic_algorithms.neat_nested import NEATNested
from .genetic_algorithms.random import RandomGA
from .genetic_algorithms.tree_ga import TreeGA


def create_ga(algorithm: Algorithm) -> GA:
    match algorithm:
        case Algorithm.RANDOM:
            return RandomGA()
        case Algorithm.BASIC:
            return BasicGA()
        case Algorithm.TREE:
            return TreeGA()
        case Algorithm.NEAT:
            return NEAT()
        case Algorithm.NEATNESTED:
            return NEATNested()
