from pathlib import Path
from typing import Type, TypeVar

import yaml
from pydantic import BaseModel, Field

from .types import Number, PathLike

T = TypeVar("T", bound=BaseModel)


class RetriesConfig(BaseModel):
    retries_count: int = 5
    retry_min_wait: Number = 0.5
    retry_max_wait: Number = 20
    suppress_error: bool = True


class RequestConfig(BaseModel):
    timeout: Number = 20


class Config(BaseModel):
    retries: RetriesConfig = Field(default_factory=RetriesConfig)
    request: RequestConfig = Field(default_factory=RequestConfig)

    @classmethod
    def from_yaml(cls: Type[T], path: PathLike = "~/.utilities.cfg") -> T:
        path = Path(path)
        if not path.exists():
            return cls()
        with open(path, mode="r") as fp:
            data = yaml.safe_load(fp)
        return cls.model_validate(data)


CFG = Config.from_yaml()
