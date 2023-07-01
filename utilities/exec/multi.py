from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Callable, List, Optional, TypeVar

from tqdm.auto import tqdm
from typing_extensions import ParamSpec

Args = ParamSpec("Args")
Input = TypeVar("Input")
Output = TypeVar("Output")


def run_th(
    items: List[Input],
    func: Callable[[Input], Output],
    n_threads: int,
    tqdm_off: bool = False,
    tqdm_leave: Optional[bool] = None,
) -> List[Output]:
    with ThreadPoolExecutor(max_workers=n_threads) as pool:
        return list(tqdm(pool.map(func, items), total=len(items), disable=tqdm_off, leave=tqdm_leave))


def run_mp(
    items: List[Input],
    func: Callable[[Input], Output],
    n_pools: int,
    tqdm_off: bool = False,
    tqdm_leave: Optional[bool] = None,
) -> List[Output]:
    with ProcessPoolExecutor(max_workers=n_pools) as pool:
        return list(tqdm(pool.map(func, items), total=len(items), disable=tqdm_off, leave=tqdm_leave))


__all__ = ["run_th", "run_mp"]
