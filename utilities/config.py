from dataclasses import dataclass, field
from pathlib import Path
from typing import Type, TypeVar

import yaml
from dacite import from_dict

from utilities.types import Number, PathLike

T = TypeVar("T")


@dataclass(frozen=True)
class RequestConfig:
    timeout: int = 20
    retries_count: int = 5
    retry_min_wait: Number = 0.5
    retry_max_wait: Number = 20
    suppress_error: bool = True


@dataclass
class Config:
    request: RequestConfig = field(default_factory=RequestConfig)

    @classmethod
    def load(cls: Type[T], path: PathLike = "~/.utilities.cfg") -> T:
        path = Path(path)
        if not path.exists():
            return cls()
        with open(path, "r") as fp:
            data = yaml.safe_load(fp)
        return from_dict(data_class=cls, data=data)


CFG = Config.load()
