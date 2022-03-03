import sys

from loguru import logger

logger.remove()


def getLogger(quiet=None, verbose=None) -> logger:  # noqa
    level = ('INFO', 'DEBUG')[bool(verbose)]
    logger.remove()

    quiet or logger.add(sys.stderr, level=level)

    return logger


def reset(verbose: int = 0, **kwargs) -> logger:  # noqa
    """
    重置 logger 等级函数

    :param verbose: 等级级别 0 - 3
    :param kwargs:
    :return:
    """

    levels = ['WARNING', 'INFO', 'DEBUG', 'TRACE']
    level0 = levels[-1] if verbose > len(levels) else levels[verbose]

    logger.remove()
    logger.add(sys.stdout, level=level0)

    return logger


def setup(verbose: int = 0, **kwargs) -> logger:  # noqa
    return reset(verbose=verbose, **kwargs)

def config(verbose: int = 0, **kwargs) -> logger:  # noqa
    return reset(verbose=verbose, **kwargs)
