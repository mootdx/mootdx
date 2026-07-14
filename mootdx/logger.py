"""Package logger without import-time duplicate handlers."""

import logging

logger = logging.getLogger("mootdx")
logger.addHandler(logging.NullHandler())
