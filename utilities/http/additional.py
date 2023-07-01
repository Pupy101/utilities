import ssl


def configure_ssl() -> None:
    try:
        unverified_https_context = ssl._create_unverified_context  # pylint: disable=protected-access
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = unverified_https_context  # pylint: disable=protected-access


__all__ = ["configure_ssl"]
