# -*- coding: utf-8 -*-
from mootdx.consts import HQ_HOSTS, EX_HOSTS, GP_HOSTS

__version__ = "0.6.7"
__author__ = "bopo.wang<ibopo@126.com>"

CONFIG = {
    'SERVER': {
        'HQ': HQ_HOSTS,
        'EX': EX_HOSTS,
        'GP': GP_HOSTS
    },
    'BESTIP': {
        'HQ': '',
        'EX': '',
        'GP': ''
    },
    'TDXDIR': 'C:/new_tdx',
}


def bestip():
    return
