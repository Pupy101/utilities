import logging
from functools import wraps
from typing import Callable, Coroutine, Optional, TypeVar

from typing_extensions import ParamSpec

from .config import CFG
from .contants import STR_ERROR_RETRIES_IMPORT

try:
    from tenacity import retry, stop_after_attempt, wait_exponential
except ImportError as exc:
    raise ImportError(STR_ERROR_RETRIES_IMPORT) from exc

logger = logging.getLogger(__file__)

A = ParamSpec("A")
O = TypeVar("O")


DEFAULT_RETRY = retry(
    wait=wait_exponential(min=CFG.retries.retry_min_wait, max=CFG.retries.retry_min_wait),
    stop=stop_after_attempt(CFG.retries.retries_count),
    reraise=True,
)


def sync_retry_supress(function: Callable[A, O]) -> Callable[A, Optional[O]]:
    @DEFAULT_RETRY
    def function_with_retry(*args: A.args, **kwargs: A.kwargs) -> O:
        return function(*args, **kwargs)

    @wraps(function)
    def inner(*args: A.args, **kwargs: A.kwargs) -> Optional[O]:
        try:
            return function_with_retry(*args, **kwargs)
        except Exception as exception:  # pylint: disable=broad-exception-caught
            logger.debug("Catch and ignored exception: %s", exception)
            if not CFG.retries.suppress_error:
                raise
            return None

    return inner


def async_retry_supress(
    function: Callable[A, Coroutine[None, None, O]],
) -> Callable[A, Coroutine[None, None, Optional[O]]]:
    @DEFAULT_RETRY
    async def function_with_retry(*args: A.args, **kwargs: A.kwargs) -> O:
        return await function(*args, **kwargs)

    @wraps(function)
    async def inner(*args: A.args, **kwargs: A.kwargs) -> Optional[O]:
        try:
            return await function_with_retry(*args, **kwargs)
        except Exception as exception:  # pylint: disable=broad-exception-caught
            logger.debug("Catch and ignored exception: %s", exception)
            if not CFG.retries.suppress_error:
                raise
            return None

    return inner
