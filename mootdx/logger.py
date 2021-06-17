from loguru import logger

log = logger

# log.add('runtime_{time}.log', format="{time} {level} {message}", filter="mootdx", level="INFO", rotation="500 MB")
# log.add(sys.stdout, filter="mootdx", level="ERROR")
