# -*- coding: utf-8 -*-
import datetime
import io
import time
from datetime import datetime, timedelta
from functools import lru_cache
from pytdx.config.hosts import hq_hosts as hosts
from pytdx.hq import TdxHq_API


def get_stock_market(symbol='', string=False):
    """判断股票ID对应的证券市场
    匹配规则
    ['50', '51', '60', '90', '110'] 为 sh
    ['00', '13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 sz
    ['5', '6', '9'] 开头的为 sh， 其余为 sz
    :param symbol:股票ID, 若以 'sz', 'sh' 开头直接返回对应类型，否则使用内置规则判断
    :return 'sh' or 'sz'"""
    assert type(symbol) is str, 'stock code need str type'

    if symbol.startswith(('sh', 'sz')):
        market = symbol[:2]

    if symbol.startswith(('50', '51', '60', '90', '110', '113', '132', '204')):
        market = 'sh'

    if symbol.startswith(('00', '13', '18', '15', '16', '18', '20', '30', '39', '115', '1318')):
        market = 'sz'

    if symbol.startswith(('5', '6', '9', '7')):
        market = 'sh'

    if string is False:
        return 0 if market == 'sz' else 1

    return market


