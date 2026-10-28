from typing import Annotated

from pydantic import BaseModel, Field

from .evolution_types import MAX_PARENTS, Algorithm, Phenotype


class GenerateRequest(BaseModel):
    algorithm: Algorithm = Algorithm.RANDOM
    parents: Annotated[list[str], Field(max_length=MAX_PARENTS)] = []

class Solution(BaseModel):
    id: str
    phenotype: Phenotype

class GenerateResponse(BaseModel):
    solutions: list[Solution]
