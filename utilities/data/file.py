import hashlib
import json
import logging
from pathlib import Path
from typing import Any, List, Optional, Union

import cv2
import numpy as np
import yaml

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


def load_image(path: PathLike) -> Optional[np.ndarray]:
    try:
        image = cv2.cvtColor(cv2.imread(str(path)), cv2.COLOR_BGR2RGB)
    except FileNotFoundError:
        image = None
    return image


def delete_file(file: PathLike) -> None:
    file = Path(file)
    if file.is_file():
        file.unlink(missing_ok=True)
    else:
        logger.warning("Can't delete not file %s", file)


def compute_md5(*, file: Optional[Union[str, Path]] = None, data: Optional[Union[str, bytes]] = None) -> str:
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


def resize_image(item: ResizeImage) -> Optional[Path]:
    path = Path(item.path)
    image = load_image(path=path)
    if image is None:
        return None
    resized_image = cv2.resize(image, item.resize(image=image))
    cv2.imwrite(str(item.path), cv2.cvtColor(resized_image, cv2.COLOR_RGB2BGR))
    return path
