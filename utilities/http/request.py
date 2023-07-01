import httpx


def check_url(url: str, verify: bool = False, timeout: int = 5) -> bool:
    try:
        response = httpx.head(url=url, verify=verify, timeout=timeout)
    except Exception:  # pylint: disable=broad-exception-caught
        return False
    return 200 <= response.status_code < 300


__all__ = ["check_url"]
