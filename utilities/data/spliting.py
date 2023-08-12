from typing import Generator, Iterable, List, TypeVar

Item = TypeVar("Item")


def chunking(items: Iterable[Item], chunk_size: int) -> Generator[List[Item], None, None]:
    chunk: List[Item] = []
    for item in items:
        chunk.append(item)
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
