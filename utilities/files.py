import hashlib
import json
import logging
from pathlib import Path
from typing import Any, List, Optional, Union, overload

import yaml

from .types import PathLike

logger = logging.getLogger(__name__)


##################################### FILE #####################################


def delete(file: PathLike) -> None:
    file = Path(file)
    if file.is_file() and file.exists():
        file.unlink(missing_ok=True)
    else:
        logger.warning("Can't delete file: '%s'", file.absolute())


@overload
def md5(*, file: PathLike, data: None = None) -> str: ...


@overload
def md5(*, file: None = None, data: Union[str, bytes]) -> str: ...


def md5(*, file=None, data=None) -> str:
    assert not (file and data) and (file or data), "Set argument file OR data"
    hasher = hashlib.md5()
    if file is not None:
        with open(file, "rb") as fp:
            while True:
                chunk = fp.read(1024)
                hasher.update(chunk)
                if not chunk:
                    break
    elif data is not None:
        assert data is not None
        if isinstance(data, str):
            data = data.encode()
        hasher.update(data)
    else:
        raise RuntimeError("Unreachable code")
    return hasher.hexdigest()


##################################### JSON #####################################


def load_json(file: PathLike) -> Any:
    with open(file, mode="r") as fp:
        return json.load(fp=fp)


def dump_json(file: PathLike, data: Any, ensure_ascii: bool = True, indent: Optional[int] = None) -> None:
    with open(file, mode="w") as fp:
        json.dump(data, fp=fp, ensure_ascii=ensure_ascii, indent=indent)


##################################### YAML #####################################


def load_yaml(file: PathLike) -> Any:
    with open(file, mode="r") as fp:
        return yaml.safe_load(stream=fp)


def dump_yaml(file: PathLike, data: Any) -> None:
    with open(file, mode="w") as fp:
        yaml.dump(data, stream=fp)


#################################### JSONL #####################################


def load_jsonl(file: PathLike) -> List[Any]:
    data: List[Any] = []
    with open(file, "r") as fp:
        for line in fp:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


def dump_jsonl(file: PathLike, data: List[Any], ensure_ascii: bool = True) -> None:
    with open(file, mode="w") as fp:
        for item in data:
            fp.write(json.dumps(item, ensure_ascii=ensure_ascii) + "\n")
