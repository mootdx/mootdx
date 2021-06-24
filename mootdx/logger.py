import sys

from loguru import logger

log = logger
log.remove()

log.add(sys.stderr, level='INFO')
