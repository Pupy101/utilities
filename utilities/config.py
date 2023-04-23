import os

RETRIES_COUNT = int(os.getenv("PY_UTILITIES_RETRIES_COUNT")) or 5  # type: ignore
