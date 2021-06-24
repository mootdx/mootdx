# -*- coding: utf-8 -*-
"""
用于管理缓存的配置数据
使用前必须先调用 init() 。
"""
import copy
import json

from unipath import Path

from mootdx.consts import EX_HOSTS, GP_HOSTS, HQ_HOSTS
from mootdx.logger import log
from mootdx.server import bestip
from mootdx.utils import get_config_path

__all__ = ['set', 'get', 'copy', 'update', 'settings']

settings = {
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

BASE = Path(__file__).parent.parent
CONF = get_config_path('config.json')


def setup():
    """
    将 yaml 里的配置文件导入到 config.py 中
    :return: bool，true 表示数据导入成功。
    """
    global settings

    try:
        options = json.load(open(CONF))
        settings.update(options)
    except Exception as e:
        log.error(e)
        log.error(f'未找到配置文件 {CONF}, 正在生成配置文件.')
        bestip()

    return True if settings else False


def has(key, value):
    """
    通过 key 设置某一项值

    :param key:
    :param value:
    :return:
    """

    return value in settings[key]


def set(key, value):
    """
    通过 key 设置某一项值

    :param key:
    :param value:
    :return:
    """

    settings[key] = value


def get(key, default=None):
    """
    通过 key 获取值

    :param key:
    :param default:
    :return:
    """

    key = key.split('.')
    cfg = settings.get(key[0])

    if len(key) > 1:
        for x in key[1:]:
            if cfg.get(x):
                cfg = cfg.get(x)
            else:
                cfg = cfg.get(x, default)
                break

    return cfg


def path(key, value=None):
    """
    通过 key 构建路径

    :param key:
    :param value:
    :return:
    """

    return Path(BASE, settings.get(key), value)


def clone():
    """
    复制配置

    :return:
    """

    return copy.deepcopy(settings)


def update(options):
    """
    全部替换配置

    :param options:
    :return:
    """

    settings.update(options)

