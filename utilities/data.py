import hashlib
from typing import Generator, Iterable, List, TypeVar, Union

Item = TypeVar("Item")


def md5(data: Union[str, bytes]) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.md5(data).hexdigest()


def chunking(items: Iterable[Item], chunk_size: int) -> Generator[List[Item], None, None]:
    chunk: List[Item] = []
    for item in items:
        chunk.append(item)
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
