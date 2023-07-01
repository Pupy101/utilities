from dataclasses import dataclass
from typing import Tuple

from PIL.Image import Image as ImageCls

from .typings import PathLike


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


__all__ = ["ResizeImage"]
