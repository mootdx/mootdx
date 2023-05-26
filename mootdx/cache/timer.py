import time
from functools import wraps


def timeit(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        delta = (time.time() - start_time)

        if delta > 1:
            t = ' '.join([str(delta), 's'])
        else:
            t = ' '.join([str(delta * 1000), 'ms'])

        print(' -> function', func.__name__, 'time:', t)
        return result

    return decorator
