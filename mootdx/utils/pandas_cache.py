import hashlib
import inspect
import time
from glob import glob
from pathlib import Path

import pandas as pd

from mootdx.cache import timeit


def file_expired(file_path, expire_seconds=3600):
    if not file_path.is_file():
        return True

    # 获取文件的stat信息
    stat_info = file_path.stat()

    # 在Unix系统中，st_ctime通常是文件的创建时间
    creation_time = stat_info.st_ctime

    # 获取当前时间
    current_time = time.time()

    # 计算文件是否过期
    expired = (current_time - creation_time) > expire_seconds
    print(f'{file_path} expired is {expired}')

    expired and Path(file_path).unlink(missing_ok=True)
    return expired


def pd_cache(cache_dir=None, expired=0):
    cache_dir = cache_dir or Path('.pd_cache')
    Path(cache_dir).mkdir(parents=True, exist_ok=True)

    def decorator(func):

        def wrapper(*args, **kw):
            # Get raw code of function as str and hash it
            func_code = ''.join(inspect.getsourcelines(func)[0])

            key = (func_code + repr(args) + repr(kw)).encode('utf8')
            hsh = hashlib.md5(key).hexdigest()[:6]

            f = cache_dir / f'{func.__name__}_{hsh}.pkl'

            if not file_expired(f, expired):
                print(f'{f} is cached')
                df = pd.read_pickle(f)
                return df

            else:
                # Delete any file name that has `cached_[func_name]_[6_chars]_.pkl`
                for cached in glob(f'{cache_dir}/{func.__name__}_*.pkl'):
                    if (len(cached) - len(func.__name__)) == 20:
                        Path(cached).unlink(missing_ok=True)

                # Write new
                df = func(*args, **kw)
                df.to_pickle(f)

                return df

        return wrapper

    return decorator


def pd_cached_delete(cache_dir=None):
    cache_dir = cache_dir or Path('.pd_cache')
    cached = glob(f'{cache_dir}/*.pkl')

    if len(cached) > 0:
        [Path(x).unlink(missing_ok=True) for x in cached]
        return f'removed {cached}'

    return 'No cached DataFrames'


if __name__ == '__main__':
    @timeit
    @pd_cache(expired=3)
    def foo():
        return pd.DataFrame([5, 54])

    @timeit
    @pd_cache(expired=5)
    def time_consuming_dataframe_operation():
        x = {i: k for i, k in enumerate(range(2 ** 16))}
        return pd.DataFrame([x])


    time_consuming_dataframe_operation()
    # pd_cached_delete()
