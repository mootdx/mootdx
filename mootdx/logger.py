import sys

from loguru import logger

log = logger
log.remove()
log.add(sink=sys.stdout, level='INFO', filter='mootdx')


def getLogger(level='INFO', **kwargs):
    log.remove()
    log.add(sink=sys.stdout, level='INFO', filter='mootdx')
