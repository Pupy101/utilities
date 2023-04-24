from pathlib import Path

import pytest

from utilities.data import ResizeImage, image_shape, resize_image

IMAGES_DIRECTORY = Path(__file__).parent / "data"


@pytest.mark.parametrize("path", IMAGES_DIRECTORY.glob("*.jpeg"))
def test_image_resize(path: Path) -> None:
    shape = image_shape(path)
    assert shape, "Can't open image"
    item = ResizeImage(path=path, size=300, check=True)
    resize_image(item)
