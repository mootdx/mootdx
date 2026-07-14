"""Small persistent DataFrame cache."""

from __future__ import annotations

import functools
import pickle
import time
from collections.abc import Callable
from pathlib import Path
from typing import ParamSpec, TypeAlias

import pandas as pd

P = ParamSpec("P")
PathLike: TypeAlias = str | Path


def file_cache(filepath: PathLike, refresh_time: float | None = None):
    """Cache a DataFrame-returning function in a pickle file.

    Corrupt and expired caches are regenerated.  The write goes through a
    temporary file so readers never observe a partially written pickle.
    """

    path = Path(filepath)

    def decorator(func: Callable[P, pd.DataFrame]):
        @functools.wraps(func)
        def retrieve_cache(*args: P.args, **kwargs: P.kwargs) -> pd.DataFrame:
            fresh = False
            try:
                fresh = refresh_time is None or path.stat().st_mtime + refresh_time >= time.time()
                if fresh:
                    cached = pd.read_pickle(path)
                    if isinstance(cached, pd.DataFrame):
                        return cached
            except (FileNotFoundError, EOFError, OSError, ValueError, pickle.UnpicklingError):
                pass

            dataframe = func(*args, **kwargs)
            if not isinstance(dataframe, pd.DataFrame):
                raise TypeError(f"{func.__name__} 必须返回 pandas.DataFrame")

            path.parent.mkdir(exist_ok=True, parents=True)
            temporary = path.with_suffix(f"{path.suffix}.tmp")
            dataframe.to_pickle(temporary)
            temporary.replace(path)
            return dataframe

        return retrieve_cache

    return decorator
