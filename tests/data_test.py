from pathlib import Path

import pytest

from utilities.vision import load_image, resize_image

DIR = Path(__file__).parent / "data"


@pytest.mark.parametrize("path", DIR.glob("*.jpeg"))
def test_image_resize(path: Path) -> None:
    image = load_image(path=path)
    assert image is not None, "Can't open image"
    output = path.with_name(path.stem + "__" + path.suffix)
    result = resize_image(path=path, size=300, output=output)
    assert result is not None, result
    new_image = load_image(path)
    assert new_image is not None, "Can't open resized image"
    new_height, new_width, _ = new_image.shape
    assert 300 in {new_height, new_width}
