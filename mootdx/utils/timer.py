import time
from functools import wraps


def timeit(func):
    """ Returns time of delta for function in seconds """

    @wraps(func)
    def timed(*args, **kw):
        ts = time.time()
        result = func(*args, **kw)

        te = time.time()
        delta = round((te - ts), 1)

        if delta > 1:
            t = ' '.join([str(delta), 's'])
        else:
            t = ' '.join([str(round((te - ts) * 1000, 1)), 'ms'])

        print('\t > function', func.__name__, 'time:', t)
        return result

    return timed


if __name__ == '__main__':
    @timeit
    def foo():
        time.sleep(0.1)


    foo()
