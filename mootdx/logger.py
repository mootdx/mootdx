import sys

from loguru import _defaults
from loguru import logger

log = logger
log.remove()
log.add(sink=sys.stderr, level='INFO', format=_defaults.LOGURU_FORMAT)


def getLogger(level='INFO', **kwargs):
    log.remove()
    log.add(sink=sys.stdout, level=level, **kwargs)
