import tempfile

import pytest


@pytest.fixture(scope="function")
def temp_dir():
    with tempfile.TemporaryDirectory() as tmp:
        yield tmp
