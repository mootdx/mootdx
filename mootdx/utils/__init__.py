# -*- coding: utf-8 -*-
import hashlib
import os
import platform
from datetime import datetime
from struct import calcsize, unpack

import pandas as pd
from pandas import DataFrame
from tqdm import tqdm
from unipath import Path

from mootdx.consts import MARKET_SH, MARKET_SZ
from mootdx.logger import log


def get_stock_markets(symbols=None):
    results = []

    assert isinstance(symbols, list), 'stock code need list type'

    if isinstance(symbols, list):
        for symbol in symbols:
            results.append([get_stock_market(symbol, string=False), symbol.strip('sh').strip('sz')])

    return results


def get_stock_market(symbol='', string=False):
    """
    判断股票ID对应的证券市场匹配规则

    ['50', '51', '60', '90', '110'] 为 sh
    ['00', '12'，'13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 sz
    ['5', '6', '9'] 开头的为 sh， 其余为 sz

    :param string: False 返回市场ID，否则市场缩写名称
    :param symbol: 股票ID, 若以 'sz', 'sh' 开头直接返回对应类型，否则使用内置规则判断
    :return 'sh' or 'sz'
    """

    assert isinstance(symbol, str), 'stock code need str type'

    market = None

    if symbol.startswith(('sh', 'sz')):
        market = symbol[:2]

    elif symbol.startswith(('50', '51', '60', '68', '90', '110', '113', '132', '204')):
        market = 'sh'

    elif symbol.startswith(('00', '12', '13', '18', '15', '16', '18', '20', '30', '39', '115', '1318')):
        market = 'sz'

    elif symbol.startswith(('5', '6', '9', '7')):
        market = 'sh'

    if string is False:
        market = MARKET_SZ if market == 'sz' else MARKET_SH

    return market


def gpcw(filepath):
    cw_file = open(filepath, 'rb')

    header_size = calcsize("<3h1H3L")
    stock_item_size = calcsize("<6s1c1L")

    data_header = cw_file.read(header_size)
    stock_header = unpack("<3h1H3L", data_header)

    max_count = stock_header[3]

    for idx in range(0, max_count):
        cw_file.seek(header_size + idx * calcsize("<6s1c1L"))
        si = cw_file.read(stock_item_size)
        stock_item = unpack("<6s1c1L", si)
        code = stock_item[0].decode()
        foa = stock_item[2]
        cw_file.seek(foa)
        info_data = cw_file.read(calcsize('<264f'))
        cw_info = unpack('<264f', info_data)

        log.debug(f"{code}, {cw_info}")
        return code, cw_info


def md5sum(downfile):
    """
    文件的 md5 哈希值

    :param downfile: 文件路径
    :return: mixed
    """

    try:
        md5_l = hashlib.md5()
        md5_l.update(Path(downfile).read_file('rb'))
        return md5_l.hexdigest()
    except (IOError, FileNotFoundError) as e:
        log.error(f'无法读取文件: {downfile}')
        log.debug(e)
        return None


def to_data(v):
    """
    数值转换为 pd.DataFrame

    :param v: mixed
    :return: pd.DataFrame
    """

    if not v:
        return pd.DataFrame(data=[])

    if isinstance(v, DataFrame):
        return v
    elif isinstance(v, list):
        return pd.DataFrame(data=v) if len(v) else None
    elif isinstance(v, dict):
        return pd.DataFrame(data=[v])

    return pd.DataFrame(data=[])


def to_file(df, filename=None):
    """
    根据扩展名输出文件

    :param df: pd.DataFrame
    :param filename: 要输出的文件，支持 csv, xlsx, xls, json, h5
    :return: bool
    """
    if filename is None or df is None:
        return None

    path_name = os.path.dirname(filename)

    if path_name and not os.path.isdir(path_name):
        os.makedirs(path_name)

    extension = os.path.splitext(filename)
    extension = extension[1] if len(extension) >= 2 else ''

    if extension == '.csv':
        return df.to_csv(filename, encoding='utf-8', index=False)
    elif extension == '.xlsx' or extension == '.xls':
        # openpyxl, xlwt
        return df.to_excel(filename, index=False)
    elif extension == '.h5':
        # tables
        return df.to_hdf(filename, 'df', index=False)
    elif extension == '.json':
        return df.to_json(filename, orient='records')

    return None


class TqdmUpTo(tqdm):
    """
    Provides `update_to(n)` which uses `tqdm.update(delta_n)`.

    """

    total: object = 0

    def update_to(self, downloaded=0, total_size=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if total_size is not None:
            self.total = total_size

        self.update(downloaded - self.n)  # will also set self.n = b * bsize


def get_config_path(config='config.json'):
    """
    获取配置文件路径

    :param config: 配置文件名称
    :return: filename
    """

    sub_path = 'mootdx' if platform.system() == 'Windows' else '.mootdx'
    filename = os.path.join(os.path.expanduser('~'), sub_path, config)
    pathname = os.path.dirname(filename)

    Path(pathname).mkdir(parents=True)

    return filename


def block_new(tdxdir=None, name: str = None, symbol: list = None):
    """
    自定义模块写入函数

    :param tdxdir: tdx 路径
    :param name: 自定义板块名称
    :param symbol: 自定义板块股票代码集合
    :return: bool
    """

    if not tdxdir:
        return False

    # 自定义板块名称未传入则自动按时间生成名称
    if not name:
        name = datetime.now().strftime('%Y%m%d%H%M%S')

    # 按时间生成 blk 文件名
    file = datetime.now().strftime('%Y%m%d%H%M%S')

    vipdoc = Path(tdxdir, 'T0002', 'blocknew')
    symbol = list(set(symbol))

    # 判断目录是否存在
    if not Path(vipdoc).isdir():
        log.error(f'自定义板块目录错误: {vipdoc}')
        return False

    block_file = Path(vipdoc, 'blocknew.cfg')

    # 文件不存在就创建
    if not block_file.exists():
        block_file.write_file('')

    # 判断名字是否重名
    with open(block_file, 'rb') as fp:
        names = fp.read().decode('gbk', 'ignore')
        names = names.split("\x00")
        names = [x for x in names if x != '']
        names = [v for i, v in enumerate(names) if i % 2 == 0]

        if name in names:
            log.error('自定义板块名称重复.')
            raise Exception('自定义板块名称重复.')

    # 写 blk 文件
    with open(f'{vipdoc}/{file}.blk', 'w') as fp:
        fp.write('\n'.join(symbol))

    # 写 blocknew.cfg 文件
    with open(block_file, 'ab') as fp:
        data = name + ((50 - len(name.encode('gbk', 'ignore'))) * "\x00")
        data += file + ((70 - len(file.encode('gbk', 'ignore'))) * "\x00")
        data = bytes(data.encode('gbk', 'ignore'))
        fp.write(data)

    return True
