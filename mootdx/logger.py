import sys

from loguru import logger, _defaults

log = logger
log.remove()
log.add(sink=sys.stderr, level="INFO", format=_defaults.LOGURU_FORMAT)


def getLogger(level='INFO', **kwargs):
    log.remove()
    log.add(sink=sys.stdout, level=level, **kwargs)
