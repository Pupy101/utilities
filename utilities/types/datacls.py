import logging
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Callable, Dict, Tuple, Type, TypeVar

from dacite import Config, from_dict

logger = logging.getLogger(__file__)

Class = TypeVar("Class")


def custom_dict_factory(ignore_none: bool) -> Callable[[Any], Dict[str, Any]]:
    def wrapper(data: Any) -> Dict[str, Any]:
        def convert(obj: Any) -> Any:
            if isinstance(obj, Enum):
                return obj.value

            return obj

        return dict((k, convert(v)) for k, v in data if not ignore_none or v is not None)

    return wrapper


@dataclass
class AsDictMixin:
    def asdict(self, ignore_attrs: Tuple[str, ...] = (), ignore_none: bool = False) -> Dict[str, Any]:
        data = asdict(self, dict_factory=custom_dict_factory(ignore_none=ignore_none))
        return {k: v for k, v in data.items() if k not in ignore_attrs}


@dataclass
class FromDictMixin:
    @classmethod
    def from_dict(cls: Type[Class], data: Dict[str, Any]) -> Class:
        return from_dict(data_class=cls, data=data, config=Config(cast=[Enum]))
