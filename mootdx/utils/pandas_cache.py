"""
Implements on disk caching of transformed dataframes

Used on a function that returns a single pandas object,
this decorator will execute the function, cache the dataframe as a pickle
file using the hash of the raw code as a unique identifier.
The next time the function runs, if the hash of the raw code matches
what is on disk, the decoratored function will simply load and return
the pickled pandas object.
This can result in speedups of 10 to 100 times, or more, depending on the
complexity of the function that creates the dataframe.

If the function changes since the last hash, this decorator will automatically delete
the previously cached pickle and save a new one, preventing disk pollutionself.
The caveat is that if the function name changes or the function is deleted, previously
cached dataframes will remain on disk. For this purpose there is a 'del_cached' function
that is will simply delete any objects cached by this decorator.
"""

import hashlib
import inspect
import logging
from functools import wraps
from glob import glob
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def pd_cache(func):
    cache_dir = Path('.pd_cache')

    logger.info(f'created `{cache_dir} dir')
    Path(cache_dir).mkdir(parents=True, exist_ok=True)

    @wraps(func)
    def cache(*args, **kw):
        # Get raw code of function as str and hash it
        func_code = ''.join(inspect.getsourcelines(func)[0])

        key = (func_code + repr(args) + repr(kw)).encode('utf8')
        hsh = hashlib.md5(key).hexdigest()[:6]

        f = f'.pd_cache/{func.__name__}_{hsh}.pkl'

        logger.info(f'\t | file {f}')

        if Path(f).exists():
            df = pd.read_pickle(f)
            logger.info(f'\t | read {f}')
            return df

        else:
            # Delete any file name that has `cached_[func_name]_[6_chars]_.pkl`
            for cached in glob(f'./.pd_cache/{func.__name__}_*.pkl'):
                if (len(cached) - len(func.__name__)) == 20:
                    Path(cached).unlink(missing_ok=True)
                    logger.info(f'\t | removed', cached)

            # Write new
            df = func(*args, **kw)

            if isinstance(df, pd.DataFrame):
                df.to_pickle(f)

            logger.info(f'\t | wrote {f}')
            return df

    return cache


def del_cached(cache_dir=None):
    cache_dir = cache_dir or Path('.pd_cache')
    cached = glob(f'{cache_dir}/*.pkl')

    if len(cached) > 0:
        [Path(x).unlink(missing_ok=True) for x in cached]
        return logger.info(f'removed {cached}')

    return 'No cached DataFrames'


if __name__ == '__main__':
    @pd_cache
    def foo():
        return pd.DataFrame([5, 54])


    foo()
    del_cached()
