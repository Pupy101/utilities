from pathlib import Path

import pytest

from utilities.data import load_image, resize_image
from utilities.types import ResizeImage

DATA_DIR = Path(__file__).parent / "data"


@pytest.mark.parametrize("path", DATA_DIR.glob("*.jpeg"))
def test_image_resize(path: Path) -> None:
    image = load_image(path=path)
    assert image is not None, "Can't open image"
    item = ResizeImage(path=path, size=300)
    resize_image(item)
    new_image = load_image(path)
    assert new_image, "Can't open resized image"
    new_height, new_width, _ = new_image
    assert new_width, new_height == item.resize(image=image)
