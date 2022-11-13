# import sys

# from loguru import logger
import logging

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)

logger = logging.getLogger("mootdx")
logger.addHandler(console)
logger.setLevel(logging.INFO)

#
# def getLogger(quiet=None, verbose=None) -> logger:  # noqa
#     level = ("INFO", "DEBUG")[bool(verbose)]
#     # logger.remove(0)
#
#     quiet or logger.add(sys.stderr, level=level)
#
#     return logger
#
#
# def reset(verbose: int = 0, **kwargs) -> logger:  # noqa
#     """
#     重置 logger 等级函数
#
#     :param verbose: 等级级别 0 - 3
#     :param kwargs:
#     :return:
#     """
#
#     levels = ["WARNING", "INFO", "DEBUG", "TRACE"]
#     level0 = levels[-1] if verbose > len(levels) else levels[verbose]
#
#     # logger.remove(0)
#     logger.add(sys.stdout, level=level0, filter="mootdx")
#     # logger.add(sys.stdout, filter=lambda record: "message" in record["extra"], format="<level>{message}</level>")
#
#     return logger
#
#
# def setup(verbose: int = 0, **kwargs) -> logger:  # noqa
#     return reset(verbose=verbose, **kwargs)
#
#
# def config(verbose: int = 0, **kwargs) -> logger:  # noqa
#     return reset(verbose=verbose, **kwargs)
