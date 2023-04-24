from pathlib import Path

import pytest

from utilities.data import ResizeImage, resize_image

IMAGES_DIRECTORY = Path(__file__).parent / "data"


@pytest.mark.parametrize("image", IMAGES_DIRECTORY.glob("*.jpeg"))
def test_image_resize(image: Path) -> None:
    pass
