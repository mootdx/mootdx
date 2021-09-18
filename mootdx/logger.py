import sys

from loguru import logger

log = logger
log.remove()
log.add(sink=sys.stdout, level='INFO')


def getLogger(level='INFO', **kwargs):
    log.remove()
    log.add(sink=sys.stdout, level=level, **kwargs)
