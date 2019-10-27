# -*- coding: utf-8 -*-
import logging
import os
from struct import *

import pandas as pd
from pandas import DataFrame

from mootdx.consts import MARKET_SZ, MARKET_SH

logger = logging.getLogger(__name__)


def get_stock_markets(symbols=None):
    results = []

    assert isinstance(symbols, list), 'stock code need list type'

    if isinstance(symbols, list):
        for symbol in symbols:
            results.append([get_stock_market(symbol, string=False), symbol])

    return results


def get_stock_market(symbol='', string=False):
    """判断股票ID对应的证券市场
    匹配规则
    ['50', '51', '60', '90', '110'] 为 sh
    ['00', '13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 sz
    ['5', '6', '9'] 开头的为 sh， 其余为 sz
    :param string:
    :param symbol:股票ID, 若以 'sz', 'sh' 开头直接返回对应类型，否则使用内置规则判断
    :return 'sh' or 'sz'"""
    assert isinstance(symbol, str), 'stock code need str type'

    market = None

    if symbol.startswith(('sh', 'sz')):
        market = symbol[:2]

    if symbol.startswith(('50', '51', '60', '90', '110', '113', '132', '204')):
        market = 'sh'

    if symbol.startswith(
        ('00',
         '13',
         '18',
         '15',
         '16',
         '18',
         '20',
         '30',
         '39',
         '115',
         '1318')):
        market = 'sz'

    if symbol.startswith(('5', '6', '9', '7')):
        market = 'sh'

    if string is False:
        # return 0 if market == 'sz' else 1
        market = MARKET_SZ if market == 'sz' else MARKET_SH

    return market


def get_ext_market(symbol='', string=False):
    """判断股票ID对应的证券市场
    匹配规则
    ['50', '51', '60', '90', '110'] 为 sh
    ['00', '13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 sz
    ['5', '6', '9'] 开头的为 sh， 其余为 sz
    :param string:
    :param symbol:股票ID, 若以 'sz', 'sh' 开头直接返回对应类型，否则使用内置规则判断
    :return 'sh' or 'sz'"""
    assert isinstance(symbol, str), 'stock code need str type'

    market = None

    if symbol.startswith(('sh', 'sz')):
        market = symbol[:2]

    if symbol.startswith(('50', '51', '60', '90', '110', '113', '132', '204')):
        market = 'sh'

    if symbol.startswith(
        ('00',
         '13',
         '18',
         '15',
         '16',
         '18',
         '20',
         '30',
         '39',
         '115',
         '1318')):
        market = 'sz'

    if symbol.startswith(('5', '6', '9', '7')):
        market = 'sh'

    if string is False:
        return 0 if market == 'sz' else 1

    return market


def parse_gpcw(filename):
    lineiter = (line.strip() for line in open(filename))
    return [line.split(',') for line in lineiter]


def gpcw(filepath):
    cw_file = open(filepath, 'rb')
    header_size = calcsize("<3h1H3L")
    stock_item_size = calcsize("<6s1c1L")
    data_header = cw_file.read(header_size)
    stock_header = unpack("<3h1H3L", data_header)
    max_count = stock_header[3]

    for stock_idx in range(0, max_count):
        cw_file.seek(header_size + stock_idx * calcsize("<6s1c1L"))
        si = cw_file.read(stock_item_size)
        stock_item = unpack("<6s1c1L", si)
        code = stock_item[0].decode()
        foa = stock_item[2]
        cw_file.seek(foa)
        info_data = cw_file.read(calcsize('<264f'))
        cw_info = unpack('<264f', info_data)

        logger.debug("{}, {}".format(code, str(cw_info)))
        return code, cw_info


def md5sum(downfile):
    import hashlib
    md5_l = hashlib.md5()
    with open(downfile, mode="rb") as f:
        by = f.read()

    md5_l.update(by)
    ret = md5_l.hexdigest()
    return ret


def to_data(v):
    if not v:
        return None

    if isinstance(v, DataFrame):
        if len(v.columns) == 0:
            return None

        return v

    if isinstance(v, list):
        return pd.DataFrame(data=v)
    elif isinstance(v, dict):
        return pd.DataFrame(data=[v, ])
    else:
        return pd.DataFrame(data=[{'value': v}])


def to_file(df, filename=None):
    if filename is None or df is None:
        return None

    extension = os.path.splitext(filename)
    extension = extension[1] if len(extension) >= 2 else ''

    if extension == 'csv':
        return df.to_csv(filename)
    elif extension == 'xlsx' or extension == 'xls':
        return df.to_excel(filename)
    elif extension == 'h5':
        return df.to_hdf(filename)
    elif extension == 'json':
        return df.to_json(filename, orient='records')

    return None
