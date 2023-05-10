import pandas as pd

from mootdx.cache import lru_cache
from mootdx.cache import timeit

NUM_SAMPLES = 100


@timeit
@lru_cache(seconds=100, maxsize=None)
def sample_function() -> pd.DataFrame:
    """Sample function that returns a constant DataFrame, for testing purpose."""
    data = {
        "ints": list(range(NUM_SAMPLES)),
        "strs": [str(i) for i in range(NUM_SAMPLES)],
        "floats": [float(i) for i in range(NUM_SAMPLES)],
    }

    return pd.DataFrame.from_dict(data)


if __name__ == '__main__':
    sample_function()
    sample_function()
