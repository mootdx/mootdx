import sys

from loguru import logger

logger.remove()


def getLogger(quiet=None, verbose=None):
    level = ('INFO', 'DEBUG')[bool(verbose)]
    logger.remove()

    quiet or logger.add(sys.stderr, level=level)

    return logger


def reset(verbose: int = 0, **kwargs) -> logger:
    """
    重置 logger 等级函数

    :param verbose: 等级级别 0 - 3
    :param kwargs:
    :return:
    """

    levels = ['WARNING', 'INFO', 'DEBUG', 'TRACE']
    levels = levels[-1] if verbose > len(levels) else levels[verbose]

    logger.remove()
    logger.add(sys.stdout, level=levels)
    return logger
