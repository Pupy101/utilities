import hashlib
import json
import logging
from pathlib import Path
from typing import Any, List, Optional, Union

import cv2
import numpy as np
import yaml

from utilities.types import PathLike

logger = logging.getLogger(__file__)


##################################### FILE #####################################


def delete(file: PathLike) -> None:
    """Delete file

    Args:
        file (`Union[str, pathlib.Path]`): path to file
    """
    file = Path(file)
    if file.is_file():
        file.unlink(missing_ok=True)
    else:
        logger.warning("Can't delete not file %s", file)


def md5(*, file: Optional[PathLike] = None, data: Optional[Union[str, bytes]] = None) -> str:
    """Compute md5 hash from file or data. Need to set argument `file` OR `data`

    Args:
        file (`Optional[Union[str, pathlib.Path]]`, optional): path to file. Defaults to `None`.
        data (`Optional[Union[str, bytes]]`, optional): data. Defaults to `None`.

    Returns:
        `str`: md5 hash
    """
    assert not (file and data) and (file or data), "Set file OR data"
    hasher = hashlib.md5()
    if file:
        with open(file, "rb") as fp:
            while True:
                chunk = fp.read(1024)
                hasher.update(chunk)
                if not chunk:
                    break
    else:
        assert data is not None
        if isinstance(data, str):
            data = data.encode()
        hasher.update(data)
    return hasher.hexdigest()


##################################### JSON #####################################


def load_json(file: PathLike) -> Any:
    """Load data from json-like file

    Args:
        file (`Union[str, pathlib.Path]`): path to json-like file

    Returns:
        `Any`: data from json-like file
    """
    with open(file, mode="r") as fp:
        return json.load(fp=fp)


def dump_json(file: PathLike, data: Any, ensure_ascii: bool = True, indent: Optional[int] = None) -> None:
    """Dump data to json-like file

    Args:
        file (`Union[str, pathlib.Path]`): path to dumping file
        data (`Any`): data for dumping
        ensure_ascii (`bool`, optional): Ensure ascii. Defaults to `True`.
        indent (`Optional[int]`, optional): Indent in dumping file. Defaults to `None`.
    """
    with open(file, mode="w") as fp:
        json.dump(data, fp=fp, ensure_ascii=ensure_ascii, indent=indent)


##################################### YAML #####################################


def load_yaml(file: PathLike) -> Any:
    """Load data from yaml-like file

    Args:
        file (`Union[str, pathlib.Path]`): path to yaml-like file

    Returns:
        `Any`: data from yaml-like file
    """
    with open(file, mode="r") as fp:
        return yaml.safe_load(stream=fp)


def dump_yaml(file: PathLike, data: Any) -> None:
    """Dump data to yaml-like file

    Args:
        file (`Union[str, pathlib.Path]`): path to dumping file
        data (`Any`): data for dumping
    """
    with open(file, mode="w") as fp:
        yaml.dump(data, stream=fp)


#################################### JSONL #####################################


def load_jsonl(file: PathLike) -> List[Any]:
    """Load data from jsonl-like file

    Args:
        file (`Union[str, pathlib.Path]`): path to jsonl-like file

    Returns:
        `List[Any]`: data from jsonl-like file
    """
    data: List[Any] = []
    with open(file, "r") as fp:
        for line in fp:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


def dump_jsonl(file: PathLike, data: List[Any], ensure_ascii: bool = True) -> None:
    """Dump data to jsonl-like file

    Args:
        file (`Union[str, pathlib.Path]`): path to dumping file
        data (`List[Any]`): data for dumping
        ensure_ascii (`bool`, optional): Ensure ascii. Defaults to True.
    """
    with open(file, mode="w") as fp:
        for item in data:
            fp.write(json.dumps(item, ensure_ascii=ensure_ascii) + "\n")


#################################### IMAGE #####################################


def load_img(path: PathLike) -> Optional[np.ndarray]:
    """Load image with opencv

    Args:
        path (`Union[str, pathlib.Path]`): path to image

    Returns:
        `Optional[numpy.ndarray]`: return `None` if file not found and otherwise `numpy.ndarray`
    """
    try:
        image = cv2.cvtColor(cv2.imread(str(path)), cv2.COLOR_BGR2RGB)
    except FileNotFoundError:
        image = None
    return image


def resize_img(path: PathLike, size: int) -> Optional[Path]:
    """Resize smallest size image to argument `size`

    Args:
        path (`Union[str, pathlib.Path]`): path to image
        size (int): target size

    Returns:
        `Optional[Path]`: return `None` if not found file otherwise `pathlib.Path`
    """
    path = Path(path)
    image = load_img(path=path)
    if image is None:
        return None
    height, width, *_ = image.shape
    if width <= height:
        new_width, new_height = size, round(size * height / width)
    else:
        new_width, new_height = round(size * width / height), size
    resized_image = cv2.resize(image, (new_width, new_height))
    cv2.imwrite(str(path), cv2.cvtColor(resized_image, cv2.COLOR_RGB2BGR))
    return path
