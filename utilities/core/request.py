import ssl
from pathlib import Path
from typing import Optional, Tuple

import httpx

from utilities.config import CFG
from utilities.types import PathLike

from .utils import sync_retry_supress


def configure_ssl() -> None:
    try:
        unverified_https_context = ssl._create_unverified_context  # pylint: disable=protected-access
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = unverified_https_context  # pylint: disable=protected-access


def check_url(url: str, verify: bool = False, timeout: int = CFG.request.timeout) -> bool:
    try:
        response = httpx.head(url=url, verify=verify, timeout=timeout)
    except Exception:  # pylint: disable=broad-exception-caught
        return False
    return 200 <= response.status_code < 300


@sync_retry_supress
def download_file(url: str, path: PathLike, chunk_size: int = 1024) -> Tuple[str, Optional[Path]]:
    path = Path(path)
    with httpx.stream(method="GET", url=url, verify=False, timeout=CFG.request.timeout) as response:
        if 200 > response.status_code or response.status_code >= 300:
            return url, None
        with open(path, "wb") as file:
            for chunk in response.iter_bytes(chunk_size=chunk_size):
                file.write(chunk)
    return url, path
