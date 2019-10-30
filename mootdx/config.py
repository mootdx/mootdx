import os
import platform


def get(key):
    return key


def set(key, val):
    return key


def values():
    if platform.system() == 'Windows':
        return os.path.join(os.environ['USER'], '_mootdx/config.josn')
    else:
        return os.path.join(os.environ['HOME'], '.mootdx/config.josn')


def setup():
    return
