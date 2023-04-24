from pathlib import Path

import pytest

from utilities.data import ResizeImage, image_shape, resize_image

IMAGES_DIRECTORY = Path(__file__).parent / "data"


@pytest.mark.parametrize("path", IMAGES_DIRECTORY.glob("*.jpeg"))
def test_image_resize(path: Path) -> None:
    old_shape = image_shape(path)
    assert old_shape, "Can't open image"
    old_width, old_height, _ = old_shape
    item = ResizeImage(path=path, size=300, check=True)
    resize_image(item)
    new_shape = image_shape(path)
    assert new_shape, "Can't open resized image"
    new_width, new_height, _ = new_shape
    assert new_width, new_height == item.resize(width=old_width, height=old_height)
