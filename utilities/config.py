import os
from typing import Any, Callable, TypeVar

Item = TypeVar("Item")


def load_env(env_name: str, transform: Callable[[Any], Item], default: Item) -> Item:
    env_value = os.getenv(env_name)
    if env_value is None:
        return default
    try:
        return transform(env_value)
    except Exception:  # pylint: disable=broad-exception-caught
        return default


RETRIES_COUNT = load_env("PY_UTILITIES_RETRIES_COUNT", int, 5)
