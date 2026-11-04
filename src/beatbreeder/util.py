import random
from typing import cast

from .evolution_types import Groove


def get_random_velocity(active_chance: float = 0.3, minimum_velocity: float = 0.3, maximum_velocity: float = 1.0) -> float:
    is_active = random.random() < active_chance
    if is_active:
        velocity = random.random()
        return minimum_velocity + velocity * (maximum_velocity - minimum_velocity)
    else:
        return 0.0

def straight_floats_to_nested_groove(flat_groove: list[list[float]]) -> Groove:
    return cast(Groove, flat_groove)

def straight_bools_to_nested_groove(straight_bools: list[list[bool]]) -> Groove:
    return [[float(b) for b in sound] for sound in straight_bools]
