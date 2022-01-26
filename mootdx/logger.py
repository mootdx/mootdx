import sys

from loguru import logger


def getLogger(quiet=None, verbose=None):
    level = ('INFO', 'DEBUG')[bool(verbose)]
    logger.remove()

    quiet or logger.add(sys.stderr, level=level)

    return logger


logger.level('TRADER', no=29, color='<green>', icon='[@]')
logger.level('VERBOSE', no=6, color='<yellow>', icon='[@]')


def reset(verbose=None, **kwargs) -> logger:
    """
    重置 logger 等级函数

    :param verbose: 等级级别 0 - 3
    :param kwargs:
    :return:
    """
    levels = ['WARNING', 'INFO', 'DEBUG', 'TRACE']
    levels = levels[-1] if verbose > len(levels) else levels[verbose]

    logger.remove()
    logger.add(sys.stdout, format='{message}', level=levels)
    logger.add('runtime/trade-{time}.log', format='{message}', level='TRADER', filter='tradebot')

    # DEBUG 日志
    verbose and logger.add('runtime/debug-{time}.log', format='{message}', level=levels, filter='tradebot')

    return logger
