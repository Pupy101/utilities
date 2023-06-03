import ssl
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Union

import httpx

from utilities.config import RETRIES_COUNT, SUPPRESS_RETRY
from utilities.data import md5
from utilities.execution import retry


def configure_ssl() -> None:
    try:
        unverified_https_context = ssl._create_unverified_context  # pylint: disable=protected-access
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = unverified_https_context  # pylint: disable=protected-access


def check_url(url: str) -> Tuple[str, bool]:
    try:
        response = httpx.head(url=url, timeout=5)
    except Exception:  # pylint: disable=broad-exception-caught
        return url, False
    return url, 200 <= response.status_code < 300


@dataclass
class DownloadItem:
    url: str
    dir: Union[str, Path]
    ext: str


@retry(count=RETRIES_COUNT, suppress=SUPPRESS_RETRY)
def download_file(item: DownloadItem) -> Tuple[str, Optional[Path]]:
    with httpx.stream("GET", item.url, verify=False, timeout=20) as response:
        if 200 > response.status_code >= 300:
            return item.url, None
        path = Path(item.dir) / f"{md5(item.url)}.{item.ext}"
        with open(path, "wb") as file:
            for chunk in response.iter_bytes(chunk_size=1024):
                file.write(chunk)
    return item.url, path
