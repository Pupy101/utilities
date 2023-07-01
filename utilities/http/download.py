import hashlib
from pathlib import Path
from typing import Optional, Tuple

import httpx

from utilities.config import CFG
from utilities.types import DownloadItem, PathLike
from utilities.utils import sync_retry_supress


def __md5(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()


@sync_retry_supress
def download_file(item: DownloadItem, directory: PathLike, chunk_size: int = 1024) -> Tuple[str, Optional[Path]]:
    with httpx.stream("GET", item.url, verify=False, timeout=CFG.request.timeout) as response:
        if 200 > response.status_code or response.status_code >= 300:
            return item.url, None
        path = Path(directory) / f"{__md5(item.url)}.{item.ext}"
        with open(path, "wb") as file:
            for chunk in response.iter_bytes(chunk_size=chunk_size):
                file.write(chunk)
    return item.url, path


__all__ = ["download_file"]
