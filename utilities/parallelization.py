from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
from typing import Callable, List, TypeVar

from tqdm.auto import tqdm

from utilities.data import chunking

Input = TypeVar("Input")
Output = TypeVar("Output")


def parallelization_th(
    func: Callable[[Input], Output],
    items: List[Input],
    n_threads: int,
    tqdm_off: bool = False,
) -> List[Output]:
    with ThreadPoolExecutor(max_workers=n_threads) as pool:
        return list(tqdm(pool.map(func, items), total=len(items), disable=tqdm_off))


def parallelization_mp(
    func: Callable[[Input], Output],
    items: List[Input],
    n_pools: int,
    tqdm_off: bool = False,
) -> List[Output]:
    with ProcessPoolExecutor(max_workers=n_pools) as pool:
        return list(tqdm(pool.map(func, items), total=len(items), disable=tqdm_off))


def parallelization_mp_th(  # pylint: disable=too-many-arguments
    func: Callable[[Input], Output],
    items: List[Input],
    n_pools: int,
    chunk_size: int,
    n_threads: int,
    tqdm_off: bool = False,
) -> List[Output]:
    func_th: Callable[[Input], List[Output]]
    func_th = partial(parallelization_th, func=func, n_threads=n_threads, tqdm_off=True)  # type: ignore
    total = round(len(items) / chunk_size)
    with ProcessPoolExecutor(max_workers=n_pools) as pool:
        outputs = list(tqdm(pool.map(func_th, chunking(items, chunk_size=chunk_size)), total=total, disable=tqdm_off))
    results: List[Output] = []
    for output in outputs:
        results.extend(output)
    return results
