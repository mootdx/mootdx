# -*- coding: utf-8 -*-
from mootdx import config
from mootdx.consts import EX_HOSTS, GP_HOSTS, HQ_HOSTS

__version__ = '0.7.1'
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


config.setup()
