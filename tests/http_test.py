from pathlib import Path

import pytest

from utilities.http import download_file
from utilities.types import DownloadItem

DATA_DIR = Path(__file__).parent / "data"


@pytest.mark.parametrize(
    "ext, status, url",
    [
        ("jpeg", True, "https://natalyland.ru/wp-content/uploads/0/1/5/015a78d68efa19fc296ba7f21bcd3c9e.jpeg"),
        ("jpeg", True, "https://dogdryg.ru/wp-content/uploads/2021/09/13-1.jpg"),
        ("jpeg", False, "https://web_that_doesn_t_exists_in_the_world_1.jpeg"),
    ],
)
def test_image_resize(ext: str, status: bool, url: str) -> None:
    item = DownloadItem(url=url, ext=ext)
    result = download_file(item, directory=DATA_DIR)
    if status:
        assert result is not None, "Retries supress"
        return_url, path = result
        assert return_url == url
        assert path is not None, "File doesn't download"
        assert path.exists(), "Not finded file"
    else:
        assert result is None
