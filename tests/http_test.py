from pathlib import Path

import pytest

from utilities.request import download_file
from utilities.types import PathLike


@pytest.mark.parametrize(
    "status, url",
    [
        (True, "https://natalyland.ru/wp-content/uploads/0/1/5/015a78d68efa19fc296ba7f21bcd3c9e.jpeg"),
        (True, "https://dogdryg.ru/wp-content/uploads/2021/09/13-1.jpg"),
        (False, "https://web_that_doesn_t_exists_in_the_world_1.jpeg"),
    ],
)
def test_image_resize(status: bool, url: str, temp_dir: PathLike) -> None:
    temp_dir = Path(temp_dir)
    path = temp_dir / Path(url).name
    result = download_file(url, path=path)
    if status:
        assert result is not None, "Retries supress"
        return_url = result
        assert return_url == url
        assert path is not None, "File doesn't download"
        assert path.exists(), "Not finded file"
    else:
        assert result is None
