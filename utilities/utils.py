import logging
from typing import Generator, Iterable, List, TypeVar

logger = logging.getLogger(__file__)


I = TypeVar("I")


def chunking(items: Iterable[I], chunk_size: int) -> Generator[List[I], None, None]:
    chunk: List[I] = []
    for item in items:
        chunk.append(item)
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
