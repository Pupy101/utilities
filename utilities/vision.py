import logging
from pathlib import Path
from typing import Optional

from utilities.contants import STR_ERROR_VISION_IMPORT
from utilities.types import PathLike

try:
    import cv2
    import numpy as np
except ImportError as exc:
    raise ImportError(STR_ERROR_VISION_IMPORT) from exc

logger = logging.getLogger(__name__)


#################################### IMAGE #####################################


def load_image(path: PathLike) -> np.ndarray:
    return cv2.cvtColor(cv2.imread(str(path)), cv2.COLOR_BGR2RGB)


def resize_image(path: PathLike, size: int, output: Optional[PathLike] = None) -> Optional[Path]:
    path = Path(path).absolute()
    output = Path(output or path).absolute()
    image = load_image(path=path)
    if image is None:
        return None
    height, width, *_ = image.shape
    if width <= height:
        new_width, new_height = size, round(size * height / width)
    else:
        new_width, new_height = round(size * width / height), size
    resized_image = cv2.resize(image, (new_width, new_height))
    cv2.imwrite(str(output), cv2.cvtColor(resized_image, cv2.COLOR_RGB2BGR))
    return output
