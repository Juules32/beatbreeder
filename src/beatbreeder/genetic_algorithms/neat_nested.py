from math import floor
from typing import override

import neat
from neat.nn.feed_forward import FeedForwardNetwork

from ..evolution_types import TRACKS, Groove, Subdivision
from .neat_ga import NEAT

MAX_DEPTH: int = 1
INITIAL_RANGE: float = 16.0
SPLITS: list[int] = [2, 3, 5, 7, 11]

class NEATNested(NEAT):
    def __init__(self, config_path: str = 'nested-cppn-config'):
        NEAT.__init__(self, config_path)

    @override
    def grooves(self) -> list[tuple[int, Groove]]:
        population: list[tuple[int, Groove]] = []
        for id, genome in self.population.population.items():
            network = neat.nn.FeedForwardNetwork.create(genome=genome, config=self.config)

            groove: Groove = []
            for instrument in range(TRACKS):
                net_wrapper = NetworkWrapper(network, instrument)
                track: Subdivision = build_subdivisions(network=net_wrapper, max_depth=MAX_DEPTH, step=0.0, step_range=INITIAL_RANGE)
                groove.append(track)
            population.append((id, groove))
        return population

class NetworkWrapper:
    def __init__(self, network: FeedForwardNetwork, instrument: int):
        self.network: FeedForwardNetwork = network
        self.instrument: int = instrument

    def activate(self, step: float) -> list[float]:
        result: list[float] = self.network.activate((self.instrument, step))
        return result

def build_subdivisions(network: NetworkWrapper, max_depth: int = 3, step: float = 0.0, step_range: float = 16.0, depth: int = 0) -> Subdivision:
    (split, velocity) = network.activate(step)
    if (depth == max_depth or split < 0.0):
        return [velocity] if velocity > 0.0 else [0.0]

    subdivision: Subdivision = []
    splits: float = SPLITS[floor(split * len(SPLITS))]
    range_per_split: float = step_range / splits

    for i in range(splits):
        sub: Subdivision = build_subdivisions(
            network=network,
            max_depth=max_depth,
            step=step + (i * range_per_split),
            step_range=range_per_split,
            depth=depth + 1
        )
        subdivision.append(sub)

    if len(subdivision) == 0:
        subdivision.append([0])

    return subdivision
