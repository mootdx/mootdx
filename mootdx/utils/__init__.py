import hashlib
from pathlib import Path
from struct import calcsize
from struct import unpack

import httpx
import pandas as pd
from pandas import DataFrame
from tqdm import tqdm

from mootdx.consts import MARKET_BJ
from mootdx.consts import MARKET_SH
from mootdx.consts import MARKET_SZ
from mootdx.logger import logger


def get_stock_markets(symbols=None):
    results = []

    assert isinstance(symbols, list), 'stock code need list type'

    if isinstance(symbols, list):
        for symbol in symbols:
            results.append([get_stock_market(symbol, string=False), symbol.strip('sh').strip('sz')])

    return results


def get_stock_market(symbol='', string=False):
    """判断股票ID对应的证券市场匹配规则

    ['50', '51', '60', '90', '110'] 为 sh
    ['00', '12'，'13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 sz
    ['5', '6', '9'] 开头的为 sh， 其余为 sz

    :param string: False 返回市场ID，否则市场缩写名称
    :param symbol: 股票ID, 若以 'sz', 'sh' 开头直接返回对应类型，否则使用内置规则判断
    :return 'sh' or 'sz'
    """

    assert isinstance(symbol, str), 'stock code need str type'

    market = 'sh'

    if symbol.startswith(('sh', 'sz', 'SH', 'SZ')):
        market = symbol[:2].lower()

    elif symbol.startswith(('50', '51', '60', '68', '90', '110', '113', '132', '204')):
        market = 'sh'

    elif symbol.startswith(('00', '12', '13', '18', '15', '16', '18', '20', '30', '39', '115', '1318')):
        market = 'sz'

    elif symbol.startswith(('5', '6', '9', '7')):
        market = 'sh'

    elif symbol.startswith(('4', '8')):
        market = 'bj'

    # logger.debug(f"market => {market}")

    if string is False:
        if market == 'sh':
            market = MARKET_SH

        if market == 'sz':
            market = MARKET_SZ

        if market == 'bj':
            market = MARKET_BJ

    # logger.debug(f"market => {market}")

    return market


def gpcw(filepath):
    cw_file = open(filepath, 'rb')

    header_size = calcsize('<3h1H3L')
    stock_item_size = calcsize('<6s1c1L')

    data_header = cw_file.read(header_size)
    stock_header = unpack('<3h1H3L', data_header)

    max_count = stock_header[3]

    for idx in range(0, max_count):
        cw_file.seek(header_size + idx * calcsize('<6s1c1L'))
        si = cw_file.read(stock_item_size)
        stock_item = unpack('<6s1c1L', si)
        code = stock_item[0].decode()
        foa = stock_item[2]
        cw_file.seek(foa)

        info_data = cw_file.read(calcsize('<264f'))
        cw_info = unpack('<264f', info_data)

        logger.debug(f'{code}, {cw_info}')
        return code, cw_info


def md5sum(downfile):
    """
    文件的 md5 哈希值

    :param downfile: 文件路径
    :return: mixed
    """

    try:
        md5_l = hashlib.md5()
        md5_l.update(Path(downfile).read_bytes())
        return md5_l.hexdigest()
    except (IOError, FileNotFoundError) as e:
        logger.warning(e)
        return None


def to_data(v, **kwargs):
    """
    数值转换为 pd.DataFrame

    :param v: mixed
    :return: pd.DataFrame
    """

    symbol = kwargs.get('symbol')
    adjust = kwargs.get('adjust', '').lower()

    if adjust in ['01', 'qfq', 'before']:
        adjust = 'qfq'
    elif adjust in ['02', 'hfq', 'after']:
        adjust = 'hfq'
    else:
        adjust = None

    # 空值
    if not isinstance(v, DataFrame) and not v:
        return pd.DataFrame(data=None)

    # DataFrame
    if isinstance(v, DataFrame):
        result = v

    # 列表
    elif isinstance(v, list):
        result = pd.DataFrame(data=v) if len(v) else None

    # 字典
    elif isinstance(v, dict):
        result = pd.DataFrame(data=[v])

    # 空值
    else:
        result = pd.DataFrame(data=[])

    if 'datetime' in result.columns:
        result.index = pd.to_datetime(result.datetime)

    if 'date' in result.columns:
        result.index = pd.to_datetime(result.date)

    if 'vol' in result.columns:
        result['volume'] = result.vol

    if adjust and adjust in ['qfq', 'hfq'] and symbol:
        from mootdx.utils.adjust import to_adjust

        result = to_adjust(result, symbol=symbol, adjust=adjust)

    # @file_cache(refresh_time=3600 * 24, filepath=get_config_path('cache/'))
    # def cache_data(data):
    #     return data

    return result


def to_file(df, filename=None):
    """
    根据扩展名输出文件

    :param df: pd.DataFrame
    :param filename: 要输出的文件，支持 csv, xlsx, xls, json, h5
    :return: bool
    """
    if filename is None or df is None:
        return None

    path_name = Path(filename).parent
    extension = Path(filename).suffix

    # 目录不存在创建目录
    Path(path_name).is_dir() or Path(path_name).mkdir(parents=True)

    # methods = {'to_json': ['.json']}
    # method = [k for k, v in methods if extension in v][0]
    # getattr(pd, method)(filename)

    if extension == '.csv':
        return df.to_csv(filename, encoding='utf-8', index=False)

    if extension == '.xlsx' or extension == '.xls':
        # openpyxl, xlwt
        return df.to_excel(filename, index=False)

    if extension == '.h5':
        # tables
        return df.to_hdf(filename, 'df', index=False)

    if extension == '.json':
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
    filename = Path.home() / '.mootdx' / config
    pathname = Path(filename).parent

    Path(pathname).exists() or Path(pathname).mkdir(parents=True)
    # Path(filename).exists() or Path(filename).write_text('None')

    return str(filename)


# days 的 vol 比 day 大 100 倍
FREQUENCY = ['5m', '15m', '30m', '1h', 'days', 'week', 'mon', 'ex_1m', '1m', 'day', '3mon', 'year']


# FREQUEN = [48,    16,   8,     4,     1,     "1/5",  "1/30", "ex_1m", 240, "1",   "1/90", "1/365"]
# FREQUENCY = ["5m", "15m", "30m", "1h", "days", "week", "mon", "ex_1m", "1m", "day", "3mon", "year"]


def get_frequency(frequency) -> int:
    # FREQUENCY = ['5m', '15m', '30m', '1h', 'day', 'week', 'mon', '1m', '1m', 'day', '3mon', 'year']

    try:
        if isinstance(frequency, str):
            frequency = FREQUENCY.index(frequency)
        if isinstance(frequency, int):
            frequency = frequency
    except ValueError:
        frequency = 0

    return frequency


def stock_bj_a() -> pd.DataFrame:
    """
    东方财富网-京 A 股-实时行情
    http://quote.eastmoney.com/center/gridlist.html#hs_a_board
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    url = 'http://82.push2.eastmoney.com/api/qt/clist/get'
    params = {
        'pn': '1',
        'pz': '50000',
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': 'm:0 t:81 s:2048',
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152',
        '_': '1623833739532',
    }

    r = httpx.get(url, params=params)
    data_json = r.json()

    if not data_json['data']['diff']:
        return pd.DataFrame()

    columns = [
        '_',
        '最新价',
        '涨跌幅',
        '涨跌额',
        '成交量',
        '成交额',
        '振幅',
        '换手率',
        '市盈率-动态',
        '量比',
        '5分钟涨跌',
        '代码',
        '_',
        '名称',
        '最高',
        '最低',
        '今开',
        '昨收',
        '总市值',
        '流通市值',
        '涨速',
        '市净率',
        '60日涨跌幅',
        '年初至今涨跌幅',
        '-',
        '-',
        '-',
        '-',
        '-',
        '-',
        '-',
    ]

    temp_df = pd.DataFrame(data_json['data']['diff'])
    temp_df.columns = columns

    temp_df.reset_index(inplace=True)
    temp_df['index'] = temp_df.index + 1

    temp_df.rename(columns={'index': '序号'}, inplace=True)
    temp_df = temp_df[[x for x in columns if x != '-']]

    for x in columns:
        if x != '-':
            temp_df[x] = pd.to_numeric(temp_df[x], errors='coerce')

    return temp_df
