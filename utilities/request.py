import ssl
from pathlib import Path
from typing import Optional

from .config import CFG
from .contants import STR_ERROR_REQUEST_IMPORT
from .types import Number, PathLike

try:
    import httpx

    from .retries import sync_retry_supress
except ImportError as exc:
    raise ImportError(STR_ERROR_REQUEST_IMPORT) from exc


def configure_ssl() -> None:
    try:
        unverified_https_context = ssl._create_unverified_context  # pylint: disable=protected-access
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = unverified_https_context  # pylint: disable=protected-access


def check_url(url: str, verify: bool = False, timeout: Number = CFG.request.timeout) -> bool:
    try:
        response = httpx.head(url=url, verify=verify, timeout=timeout)
    except Exception:  # pylint: disable=broad-exception-caught
        return False
    return 200 <= response.status_code < 300


@sync_retry_supress
def download_file(url: str, path: PathLike, chunk_size: int = 1024 * 1024) -> Optional[Path]:
    path = Path(path)
    with httpx.stream(method="GET", url=url, verify=False, timeout=CFG.request.timeout) as response:
        if 200 > response.status_code or response.status_code >= 300:
            return None
        with open(path, "wb") as file:
            for chunk in response.iter_bytes(chunk_size=chunk_size):
                file.write(chunk)
    return path
