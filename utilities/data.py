import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generator, Iterable, List, Optional, Tuple, TypeVar, Union

import pandas as pd
import yaml
from PIL import Image, UnidentifiedImageError
from PIL.Image import Image as ImageCls
from sklearn.model_selection import train_test_split

Item = TypeVar("Item")
PathLike = Union[str, Path]


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


def delete_file(file: PathLike) -> None:
    try:
        Path(file).unlink(missing_ok=True)
    except Exception:  # pylint: disable=broad-exception-caught
        pass


def md5(data: Union[str, bytes]) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.md5(data).hexdigest()


@dataclass
class ResizeImage:
    path: PathLike
    size: int
    check: bool = True

    def resize(self, image: ImageCls) -> Tuple[int, int]:
        width, height = image.width, image.height
        if width <= height:
            resized_width, resized_height = self.size, round(self.size * height / width)
        else:
            resized_width, resized_height = round(self.size * width / height), self.size
        return (resized_width, resized_height)


def read_image(path: PathLike) -> Optional[ImageCls]:
    try:
        image = Image.open(path)
    except (FileNotFoundError, ValueError, TypeError, UnidentifiedImageError, Image.DecompressionBombError):
        image = None
    return image


def image_shape(path: PathLike) -> Optional[Tuple[int, int, int]]:
    image = read_image(path=path)
    if image is not None:
        return image.width, image.height, len(image.mode)
    return None


def resize_image(item: ResizeImage) -> Tuple[Path, bool]:
    path = Path(item.path)
    image = read_image(path=path)
    if image is not None:
        channels = len(image.mode)
        try:
            image.resize(item.resize(image=image), Image.LANCZOS).save(path)
            force_delete = False
        except Exception:  # pylint: disable=broad-exception-caught
            force_delete = True
    else:
        force_delete = True
    if force_delete or item.check and channels != 3:
        delete_file(file=path)
        return path, False
    return path, True


def chunking(items: Iterable[Item], chunk_size: int) -> Generator[List[Item], None, None]:
    chunk: List[Item] = []
    for item in items:
        chunk.append(item)
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def train_valid_test_split(
    data: pd.DataFrame,
    valid_size: float,
    test_size: float,
    random_state: int = 42,
    stratify_column: Optional[str] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    assert valid_size + test_size < 1, "Sum of valid/test sizes must be smaller 1"
    if stratify_column:
        assert stratify_column in data.columns, f"Column {stratify_column} must be in dataframe"
    stratify = data[stratify_column] if stratify_column else None
    train_valid_df, test_df = train_test_split(
        data,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify,
    )
    stratify = train_valid_df[stratify_column] if stratify_column else None
    train_df, valid_df = train_test_split(
        train_valid_df,
        test_size=valid_size / (1 - test_size),
        random_state=random_state,
        stratify=stratify,
    )
    return train_df, valid_df, test_df
