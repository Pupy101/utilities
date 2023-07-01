import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Any, Callable, Coroutine, Iterable, List, Optional, TypeVar

from tqdm.auto import tqdm
from typing_extensions import ParamSpec

Args = ParamSpec("Args")
Input = TypeVar("Input")
Output = TypeVar("Output")


def run_th(
    items: Iterable[Input],
    func: Callable[[Input], Output],
    n_threads: int,
    tqdm_off: bool = False,
    tqdm_leave: Optional[bool] = None,
) -> List[Output]:
    with ThreadPoolExecutor(max_workers=n_threads) as pool:
        return list(tqdm(pool.map(func, items), disable=tqdm_off, leave=tqdm_leave))


def run_mp(
    items: Iterable[Input],
    func: Callable[[Input], Output],
    n_pools: int,
    tqdm_off: bool = False,
    tqdm_leave: Optional[bool] = None,
) -> List[Output]:
    with ProcessPoolExecutor(max_workers=n_pools) as pool:
        return list(tqdm(pool.map(func, items), disable=tqdm_off, leave=tqdm_leave))


async def run_aio(
    items: Iterable[Input],
    afunc: Callable[[Input], Coroutine[Any, Any, Output]],
    n_workers: int,
    tqdm_off: bool = False,
    tqdm_leave: Optional[bool] = None,
) -> List[Output]:
    semaphore = asyncio.Semaphore(n_workers)
    tasks = [afunc(_) for _ in items]

    async def worker_wrapper(task: Coroutine[Any, Any, Output], p_bar: tqdm) -> Output:
        async with semaphore:
            p_bar.update()
            return await task

    with tqdm(disable=tqdm_off, leave=tqdm_leave) as p_bar:
        return await asyncio.gather(*[worker_wrapper(task, p_bar=p_bar) for task in tasks])


__all__ = ["run_th", "run_mp", "run_aio"]
