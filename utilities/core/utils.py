import logging
from functools import wraps
from typing import Callable, Coroutine, Generator, Iterable, List, Optional, TypeVar

from tenacity import retry, stop_after_attempt, wait_exponential
from typing_extensions import ParamSpec

from utilities.config import CFG

logger = logging.getLogger(__file__)

Args = ParamSpec("Args")
Output = TypeVar("Output")
Item = TypeVar("Item")


DEFAULT_RETRY = retry(
    wait=wait_exponential(min=CFG.request.retry_min_wait, max=CFG.request.retry_min_wait),
    stop=stop_after_attempt(CFG.request.retries_count),
    reraise=True,
)


def sync_retry_supress(function: Callable[Args, Output]) -> Callable[Args, Optional[Output]]:
    @DEFAULT_RETRY
    def function_with_retry(*args: Args.args, **kwargs: Args.kwargs) -> Output:
        return function(*args, **kwargs)

    @wraps(function)
    def inner(*args: Args.args, **kwargs: Args.kwargs) -> Optional[Output]:
        try:
            return function_with_retry(*args, **kwargs)
        except Exception as exception:  # pylint: disable=broad-exception-caught
            logger.debug("Catch and ignored exception: %s", exception)
            if not CFG.request.suppress_error:
                raise
            return None

    return inner


def async_retry_supress(
    function: Callable[Args, Coroutine[None, None, Output]]
) -> Callable[Args, Coroutine[None, None, Optional[Output]]]:
    @DEFAULT_RETRY
    async def function_with_retry(*args: Args.args, **kwargs: Args.kwargs) -> Output:
        return await function(*args, **kwargs)

    @wraps(function)
    async def inner(*args: Args.args, **kwargs: Args.kwargs) -> Optional[Output]:
        try:
            return await function_with_retry(*args, **kwargs)
        except Exception as exception:  # pylint: disable=broad-exception-caught
            logger.debug("Catch and ignored exception: %s", exception)
            if not CFG.request.suppress_error:
                raise
            return None

    return inner


def chunking(items: Iterable[Item], chunk_size: int) -> Generator[List[Item], None, None]:
    """Create generator with chunks from iterable

    Args:
        items (`Iterable[Item]`): iterable for chunking
        chunk_size (`int`): chunk size

    Yields:
        `List[Item]`: chunk with items
    """
    chunk: List[Item] = []
    for item in items:
        chunk.append(item)
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
