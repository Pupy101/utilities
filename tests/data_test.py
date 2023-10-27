from pathlib import Path

import pytest

from utilities.core import load_img, resize_img

DATA_DIR = Path(__file__).parent / "data"


@pytest.mark.parametrize("path", DATA_DIR.glob("*.jpeg"))
def test_image_resize(path: Path) -> None:
    image = load_img(path=path)
    assert image is not None, "Can't open image"
    resize_img(path=path, size=300)
    new_image = load_img(path)
    assert new_image is not None, "Can't open resized image"
    new_height, new_width, _ = new_image.shape
    assert 300 in {new_height, new_width}
