from typing import Any
from typing_extensions import TypedDict

from pydantic import BaseModel, ConfigDict


class Step(TypedDict):
    step: str
    duration: float


class Results(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    metadata_name: str
    metadata: dict
    nsteps: int
    current_step: int
    output: Any
    len_output: int | None
    total_duration: float
    output_recap: tuple[Step, ...]
