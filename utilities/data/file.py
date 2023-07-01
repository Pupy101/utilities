import hashlib
import json
import logging
from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

import yaml
from PIL import Image, UnidentifiedImageError
from PIL.Image import Image as ImageCls

from utilities.types import PathLike, ResizeImage

logger = logging.getLogger(__file__)


def load_yaml(file: PathLike) -> Any:
    with open(file, "r") as fp:
        return yaml.safe_load(fp)


def load_json(file: PathLike) -> Any:
    with open(file, "r") as fp:
        return json.load(fp)


def load_jsonl(file: PathLike) -> List[Any]:
    data: List[Any] = []
    with open(file, "r") as fp:
        for line in fp:
            data.append(json.loads(line))
    return data


def load_image(path: PathLike) -> Optional[ImageCls]:
    try:
        image = Image.open(path)
    except (FileNotFoundError, ValueError, TypeError, UnidentifiedImageError, Image.DecompressionBombError):
        image = None
    return image


def delete_file(file: PathLike) -> None:
    file = Path(file)
    if file.is_file():
        file.unlink(missing_ok=True)
    else:
        logger.warning("Can't delete directory %s", file)


def compute_md5_hash(data: Union[str, bytes]) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.md5(data).hexdigest()


def image_shape(path: PathLike) -> Optional[Tuple[int, int, int]]:
    image = load_image(path=path)
    if image is not None:
        return image.width, image.height, len(image.mode)
    return None


def resize_image(item: ResizeImage) -> Optional[Path]:
    path = Path(item.path)
    image = load_image(path=path)
    if image is not None:
        channels = len(image.mode)
        try:
            image.resize(item.resize(image=image), Image.LANCZOS).save(path)
            delete = False
        except Exception:  # pylint: disable=broad-exception-caught
            delete = True
            channels = 0
    else:
        delete = True
        channels = 0
    if delete or item.check and channels != 3:
        delete_file(file=path)
        return None
    return path


__all__ = [
    "load_yaml",
    "load_json",
    "load_jsonl",
    "load_image",
    "delete_file",
    "compute_md5_hash",
    "image_shape",
    "resize_image",
]
