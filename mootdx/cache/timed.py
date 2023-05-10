import functools
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Callable
from typing import cast
from typing import Optional
from typing import Protocol

import pandas as pd

from .compat import ParamSpec
from .compat import TypeAlias

P = ParamSpec('P')

PandasFunc: TypeAlias = Callable[P, pd.DataFrame]


class LRUCacheWrapper(Protocol[P]):
    lifetime: timedelta
    expiration: datetime

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> pd.DataFrame:
        pass

    def clear(self):
        pass


def lru_cache(seconds: Optional[int] = None, maxsize: Optional[int] = None, typed: bool = True):
    """
    装饰器工厂，生成一个装饰器，该装饰器在内存中缓存熊猫数据帧（具有一定的过期时间），以便将来更快地检索.

    :param seconds: 保留缓存的秒数
    :param maxsize: 要存储在缓存中的最大项目数
    :param typed: 不同类型的参数是否将单独缓存
    :return: 在内存中缓存 pd.DataFrame 的装饰器（含过期时间）.
    """

    def decorator(func: PandasFunc) -> PandasFunc:
        lru_func = cast(LRUCacheWrapper, functools.lru_cache(maxsize=maxsize, typed=typed)(func))

        if not seconds:
            return lru_func

        lru_func.lifetime = timedelta(seconds=seconds)
        lru_func.expiration = datetime.now(timezone.utc) + lru_func.lifetime

        @functools.wraps(func)
        def retrieve_cache(*args: P.args, **kwargs: P.kwargs) -> pd.DataFrame:
            if datetime.now(timezone.utc) >= lru_func.expiration:
                lru_func.clear()
                lru_func.expiration = datetime.now(timezone.utc) + lru_func.lifetime

            return lru_func(*args, **kwargs)

        return cast(PandasFunc, retrieve_cache)

    return decorator
