from pathlib import Path
from typing import List, Optional

from setuptools import find_packages, setup

DIR = Path(__file__).parent / "requirements"
EXCLUDE = ["tests"]


def read_file(file: Path) -> List[str]:
    lines: List[str] = []
    with open(file) as fp:
        for line in fp:
            line = line.strip()
            if line:
                lines.append(line)
    return lines


def read_requirements(options: Optional[List[str]] = None) -> List[str]:
    options = options or []
    options.append("default")  # add default option
    options = list(set(options))

    requirements: List[str] = []
    for option in options:
        file = DIR / f"{option}.txt"
        assert file.exists(), f"Not found file: {file.absolute()}"
        requirements.extend(read_file(file=file))

    assert requirements, "Empty requirements"
    return requirements


EXTRAS_REQUIRE = {
    "dev": read_requirements(options=["dev"]),
    "vision": read_requirements(options=["vision"]),
    "retries": read_requirements(options=["retries"]),
    "request": read_requirements(options=["request", "retries"]),
}
EXTRAS_REQUIRE["full"] = list({_ for option_requeres in EXTRAS_REQUIRE.values() for _ in option_requeres})


setup(
    name="utilities",
    version="0.1.4",
    description="Library with python utilities",
    author="Sergei Porkhun",
    author_email="ser.porkhun41@gmail.com",
    packages=find_packages(exclude=EXCLUDE),
    install_requires=read_requirements(),
    extras_require=EXTRAS_REQUIRE,
)
