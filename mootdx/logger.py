import sys

from loguru import logger


def getLogger(quiet=None, verbose=None):
    level = ('INFO', 'DEBUG')[bool(verbose)]
    logger.remove()

    quiet or logger.add(sys.stderr, level=level)

    return logger


log = getLogger()
