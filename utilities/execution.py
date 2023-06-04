from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial, wraps
from typing import Callable, List, Literal, Optional, TypeVar, overload

from tqdm.auto import tqdm
from typing_extensions import ParamSpec

from utilities.data import chunking

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


def run_mp_th(  # pylint: disable=too-many-arguments
    items: List[Input],
    func: Callable[[Input], Output],
    n_pools: int,
    chunk_size: int,
    n_threads: int,
    tqdm_off: bool = False,
    tqdm_leave: Optional[bool] = None,
) -> List[Output]:
    func_th: Callable[[Input], List[Output]]
    func_th = partial(run_th, func=func, n_threads=n_threads, tqdm_off=True)  # type: ignore
    total = round(len(items) / chunk_size)
    with ProcessPoolExecutor(max_workers=n_pools) as pool:
        outputs = list(
            tqdm(
                pool.map(func_th, chunking(items, chunk_size=chunk_size)),
                total=total,
                disable=tqdm_off,
                leave=tqdm_leave,
            )
        )
    results: List[Output] = []
    for output in outputs:
        results.extend(output)
    return results


@overload
def retry(count: int, suppress: Literal[True]) -> Callable[[Callable[Args, Output]], Callable[Args, Optional[Output]]]:
    ...


@overload
def retry(count: int, suppress: Literal[False]) -> Callable[[Callable[Args, Output]], Callable[Args, Output]]:
    ...


def retry(count: int, suppress: bool):
    def decorator(func: Callable[Args, Output]):
        @wraps(func)
        def wrapper(*args: Args.args, **kwargs: Args.kwargs):  # pylint: disable=inconsistent-return-statements
            for i in range(count + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:  # pylint: disable=broad-exception-caught
                    if i < count:
                        continue
                    if not suppress:
                        raise

        return wrapper

    return decorator
