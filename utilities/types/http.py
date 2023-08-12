from dataclasses import dataclass


@dataclass
class DownloadItem:
    url: str
    ext: str
