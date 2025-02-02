import asyncio
import logging
from multiprocessing.pool import Pool, ThreadPool
from typing import Any, Callable, Coroutine, Iterable, List, Optional, Tuple, TypeVar

from tqdm.auto import tqdm

logger = logging.getLogger(__name__)

I = TypeVar("I")
O = TypeVar("O")


def run_threads(
    items: Iterable[I],
    func: Callable[[I], O],
    n_threads: int,
    tqdm_off: bool = False,
    tqdm_leave: Optional[bool] = None,
) -> List[Tuple[I, O]]:
    items = list(items)
    n_threads = min(n_threads, len(items))
    assert n_threads >= 1, n_threads

    with ThreadPool(processes=n_threads) as pool:
        return list(zip(items, tqdm(pool.imap(func, items), total=len(items), disable=tqdm_off, leave=tqdm_leave)))


def run_processes(
    items: Iterable[I],
    func: Callable[[I], O],
    n_processes: int,
    tqdm_off: bool = False,
    tqdm_leave: Optional[bool] = None,
) -> List[Tuple[I, O]]:
    items = list(items)
    n_processes = min(n_processes, len(items))
    assert n_processes >= 1, n_processes

    with Pool(processes=n_processes) as pool:
        return list(zip(items, tqdm(pool.map(func, items), total=len(items), disable=tqdm_off, leave=tqdm_leave)))


async def run_async(
    items: Iterable[I],
    afunc: Callable[[I], Coroutine[Any, Any, O]],
    n_workers: int,
    tqdm_off: bool = False,
    tqdm_leave: bool = False,
) -> List[Tuple[I, O]]:
    semaphore = asyncio.Semaphore(n_workers)
    items = list(items)
    n_workers = min(n_workers, len(items))
    assert n_workers >= 1, n_workers

    progress_bar = tqdm(total=len(items), disable=tqdm_off, leave=tqdm_leave)

    async def worker(item: I) -> O:
        async with semaphore:
            try:
                result = await afunc(item)
                return result
            finally:
                progress_bar.update(n=1)

    try:
        results = await asyncio.gather(*[worker(item) for item in items])
    finally:
        progress_bar.close()

    return list(zip(items, results))
