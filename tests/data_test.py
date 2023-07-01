from pathlib import Path

import pytest

from utilities.data import image_shape, load_image, resize_image
from utilities.types import ResizeImage

DATA_DIR = Path(__file__).parent / "data"


@pytest.mark.parametrize("path", DATA_DIR.glob("*.jpeg"))
def test_image_resize(path: Path) -> None:
    image = load_image(path=path)
    old_shape = image_shape(path)
    assert old_shape, "Can't open image"
    item = ResizeImage(path=path, size=300, check=True)
    resize_image(item)
    new_shape = image_shape(path)
    assert new_shape, "Can't open resized image"
    new_width, new_height, _ = new_shape
    assert new_width, new_height == item.resize(image=image)
