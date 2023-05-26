import functools
import os
import pathlib
import time
from typing import Callable
from typing import Optional
from typing import Union

import pandas as pd

from ..exceptions import FileNeedRefresh
from .compat import ParamSpec
from .compat import TypeAlias

P = ParamSpec('P')

PathLike: TypeAlias = Union[str, pathlib.Path]


def file_cache(filepath: PathLike, refresh_time: Optional[float] = None):
    def decorator(func: Callable[P, pd.DataFrame]):
        @functools.wraps(func)
        def retrieve_cache(*args: P.args, **kwargs: P.kwargs):
            try:
                if refresh_time is not None and os.path.getmtime(filepath) + int(refresh_time) < time.time():
                    raise FileNeedRefresh(f'{filepath} 太旧，需要刷新')
                dataframe: pd.DataFrame = pd.read_pickle(filepath)
            except (FileNotFoundError, EOFError):
                pathlib.Path(filepath).parent.mkdir(exist_ok=True, parents=True)

                dataframe = func(*args, **kwargs)
                dataframe.to_pickle(filepath)

            return dataframe

        return retrieve_cache

    return decorator
