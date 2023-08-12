from dataclasses import dataclass
from typing import Tuple

import numpy as np

from .typings import PathLike


@dataclass
class ResizeImage:
    path: PathLike
    size: int

    def resize(self, image: np.ndarray) -> Tuple[int, int]:
        height, width, *_ = image.shape
        if width <= height:
            resized_width, resized_height = self.size, round(self.size * height / width)
        else:
            resized_width, resized_height = round(self.size * width / height), self.size
        return (resized_width, resized_height)
