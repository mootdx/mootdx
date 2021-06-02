from loguru import logger as log

log.add('runtime_{time}.log', format="{time} {level} {message}", filter="mootdx", level="INFO", rotation="500 MB")
