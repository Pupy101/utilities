from typing import Generator, Iterable, List, Optional, Tuple, TypeVar

import pandas as pd
from sklearn.model_selection import train_test_split

Item = TypeVar("Item")


def chunking(items: Iterable[Item], chunk_size: int) -> Generator[List[Item], None, None]:
    chunk: List[Item] = []
    for item in items:
        chunk.append(item)
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def train_valid_test_split(
    data: pd.DataFrame,
    valid_size: float,
    test_size: float,
    random_state: int = 42,
    stratify_column: Optional[str] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    assert valid_size + test_size < 1, "Sum of valid/test sizes must be smaller 1"
    if stratify_column:
        assert stratify_column in data.columns, f"Column {stratify_column} must be in dataframe"
    stratify = data[stratify_column] if stratify_column else None
    train_valid_df, test_df = train_test_split(
        data,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify,
    )
    stratify = train_valid_df[stratify_column] if stratify_column else None
    train_df, valid_df = train_test_split(
        train_valid_df,
        test_size=valid_size / (1 - test_size),
        random_state=random_state,
        stratify=stratify,
    )
    return train_df, valid_df, test_df


__all__ = ["chunking", "train_valid_test_split"]
