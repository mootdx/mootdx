# -*- coding: utf-8 -*-

from mootdx import config
from mootdx.consts import EX_HOSTS, GP_HOSTS, HQ_HOSTS

__version__ = '0.7.2'
__author__ = "bopo.wang<ibopo@126.com>"

from mootdx.server import Server

from mootdx.utils import get_config_path



config.setup()
