import warnings
from pathlib import Path
from typing import List

from setuptools import find_packages, setup

EXCLUDED_PACKAGES = ["*tests*"]


def dev_requirements() -> List[str]:
    return ["black", "isort", "mypy", "pylint", "pytest"]


def find_requirements() -> List[str]:
    requirements_txt = Path(__file__).parent / "requiresment.txt"
    requirements = []
    if requirements_txt.exists():
        with open(requirements_txt, "r", encoding="utf-8") as req_file:
            for line in req_file:
                requirements.append(line.strip())
    else:
        warnings.warn(f"Not found file '{requirements_txt}' with requiresments")
    return requirements


setup(
    name="utilities",
    version="0.1",
    description="Library with python utilities",
    author="Sergei Porkhun",
    author_email="ser.porkhun41@gmail.com",
    packages=find_packages(exclude=EXCLUDED_PACKAGES),
    install_requires=find_requirements(),
    extras_require={"dev": find_requirements() + dev_requirements()},
)
