import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generator, Iterable, List, Tuple, TypeVar, Union

import yaml
from PIL import Image

Item = TypeVar("Item")


def load_yaml(file: Union[str, Path]) -> Any:
    with open(file, "r") as fp:
        return yaml.safe_load(fp)


def load_json(file: Union[str, Path]) -> Any:
    with open(file, "r") as fp:
        return json.load(fp)


def load_jsonl(file: Union[str, Path]) -> List[Any]:
    data: List[Any] = []
    with open(file, "r") as fp:
        for line in fp:
            data.append(json.loads(line))
    return data


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


@dataclass
class ResizeImage:
    path: Union[str, Path]
    size: int
    check: bool = True


def resize_image(item: ResizeImage) -> Tuple[Path, bool]:
    path = Path(item.path)
    if not path.exists():
        return path, False
    image = Image.open(path)
    width, height, channels = image.width, image.height, len(image.mode)
    if item.check and channels != 3:
        try:
            path.unlink()
        except Exception:  # pylint: disable=broad-exception-caught
            return path, False
    if width <= height:
        width, height = item.size, round(item.size * height / width)
    else:
        width, height = round(item.size * width / height), item.size
    shape = (width, height)
    resized_image = image.resize(shape, Image.ANTIALIAS)
    resized_image.save(path)
    return path, True
