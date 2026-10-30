from typing import Annotated

from pydantic import BaseModel, Field

from .evolution_types import MAX_PARENTS, POPULATION_SIZE, Algorithm, Groove


class GenerateRequest(BaseModel):
    algorithm: Algorithm = Algorithm.RANDOM
    gid: str | None = None
    pids: Annotated[list[int], Field(max_length=MAX_PARENTS)] = []

class GenerateResponse(BaseModel):
    gid: str
    grooves: Annotated[list[tuple[int, Groove]], Field(max_length=POPULATION_SIZE)]
