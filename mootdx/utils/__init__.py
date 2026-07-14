import hashlib
import re
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

# 默认请求超时（秒）
_DEFAULT_TIMEOUT = httpx.Timeout(10.0, connect=5.0)


def _normalize_symbol(symbol: str) -> tuple[str | None, str]:
    if not isinstance(symbol, str):
        raise TypeError('stock code must be a string')
    normalized = symbol.strip().upper()
    if not normalized:
        raise ValueError('stock code cannot be empty')

    match = re.fullmatch(r'(?:(SH|SZ|BJ)[.#]?)?([0-9A-Z]+)', normalized)
    if not match:
        raise ValueError(f'无效证券代码: {symbol!r}')
    return match.group(1), match.group(2)


def get_stock_markets(symbols=None):
    """Normalize a collection of security codes for ``tdxpy``.

    ``tdxpy`` expects ``(market, code)`` pairs, while callers commonly pass
    prefixed codes such as ``SH.600000``.  Keep accepting lists and tuples for
    backwards compatibility, but reject strings explicitly so a single code
    is not accidentally iterated character by character.
    """
    if isinstance(symbols, str) or not isinstance(symbols, (list, tuple)):
        raise TypeError('stock codes must be a list or tuple')
    return [[get_stock_market(symbol), _normalize_symbol(symbol)[1]] for symbol in symbols]

def get_stock_market(symbol='', string=False):
    """
    最新A股6位编码市场判断（兼容北交所920新规、沪深全品种）
    :param symbol: 证券代码，支持SH600000 / SZ300750 / 纯数字
    :param string: True返回sh/sz/bj字符串，False返回市场数字常量
    """
    prefix, symbol = _normalize_symbol(symbol)
    market = prefix.lower() if prefix else 'sz'

    # 优先级1：自带SH/SZ/BJ前缀直接判定
    if prefix is None:
        # 北交所 920 专属号段（最高优先级）
        if symbol.startswith("920"):
            market = "bj"
        # 上交所SH 前缀全集（支持两位和三位）
        elif symbol.startswith(("60", "68", "50", "51", "110", "113", "132", "204", "90")):
            market = "sh"
        # 深市逆回购特殊四位前缀，避免被13前缀误判（必须放在sz前缀之前）
        elif symbol.startswith("1318"):
            market = "sz"
        # 深交所SZ 两位前缀全集
        elif len(symbol) >= 2 and symbol[:2] in {"00", "12", "13", "15", "16", "18", "20", "30", "39"}:
            market = "sz"
        # 老三板、新三板 4/8开头归北交所（北交所股票以8开头，部分4开头也归此）
        elif symbol.startswith(("4", "8")):
            market = "bj"
        # 其余未匹配的均保持默认深圳（sz）

    # 返回格式转换
    if string:
        return market
    return {'sh': MARKET_SH, 'sz': MARKET_SZ, 'bj': MARKET_BJ}[market]

def gpcw(filepath):
    header_format = '<3hH3L'
    item_format = '<6scL'
    header_size = calcsize(header_format)
    item_size = calcsize(item_format)
    info_size = calcsize('<264f')

    with Path(filepath).open('rb') as cw_file:
        data_header = cw_file.read(header_size)
        if len(data_header) != header_size:
            raise ValueError('财务文件头不完整')
        max_count = unpack(header_format, data_header)[3]

        results = []
        for idx in range(max_count):
            cw_file.seek(header_size + idx * item_size)
            item = cw_file.read(item_size)
            if len(item) != item_size:
                raise ValueError(f'第 {idx} 条财务索引不完整')
            stock_item = unpack(item_format, item)
            code = stock_item[0].decode('ascii').rstrip('\x00')
            cw_file.seek(stock_item[2])
            info_data = cw_file.read(info_size)
            if len(info_data) != info_size:
                raise ValueError(f'{code} 的财务记录不完整')
            results.append((code, unpack('<264f', info_data)))

    return results


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
    adjust = str(kwargs.get('adjust') or '').lower()

    if adjust in ['01', 'qfq', 'before']:
        adjust = 'qfq'
    elif adjust in ['02', 'hfq', 'after']:
        adjust = 'hfq'
    else:
        adjust = None

    # Avoid ``if not value`` here: NumPy arrays and pandas Series deliberately
    # reject ambiguous truth-value checks.
    if v is None:
        return pd.DataFrame()
    if isinstance(v, DataFrame):
        result = v.copy()
    elif isinstance(v, dict):
        result = pd.DataFrame([v]) if v else pd.DataFrame()
    elif isinstance(v, (list, tuple)):
        result = pd.DataFrame(v) if len(v) else pd.DataFrame()
    else:
        # Some tdxpy versions return a NumPy array or another tabular object.
        # Let pandas handle it, but consistently return an empty frame for
        # scalar/unsupported values instead of raising from a truth check.
        try:
            result = pd.DataFrame(v)
        except (TypeError, ValueError):
            return pd.DataFrame()
        if result.empty and not hasattr(v, "columns"):
            return result

    if 'datetime' in result.columns:
        result.index = pd.to_datetime(result['datetime'], errors='coerce')
    elif 'date' in result.columns:
        result.index = pd.to_datetime(result['date'], errors='coerce')

    if 'vol' in result.columns and 'volume' not in result.columns:
        result['volume'] = result['vol']

    if adjust and adjust in ['qfq', 'hfq'] and symbol:
        from mootdx.utils.adjust import to_adjust

        result = to_adjust(result, symbol=symbol, adjust=adjust, xdxr=kwargs.get('xdxr'))

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
    Path(path_name).mkdir(parents=True, exist_ok=True)

    # methods = {'to_json': ['.json']}
    # method = [k for k, v in methods if extension in v][0]
    # getattr(pd, method)(filename)

    extension = extension.lower()
    if extension == '.csv':
        return df.to_csv(filename, encoding='utf-8', index=False)

    if extension in {'.xlsx', '.xls'}:
        # openpyxl, xlwt
        return df.to_excel(filename, index=False)

    if extension == '.h5':
        # tables
        return df.to_hdf(filename, 'df', index=False)

    if extension == '.json':
        return df.to_json(filename, orient='records')

    raise ValueError(f'不支持的输出格式: {extension or "<none>"}')


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

    Path(pathname).mkdir(parents=True, exist_ok=True)
    # Path(filename).exists() or Path(filename).write_text('None')

    return str(filename)


# days 的 vol 比 day 大 100 倍
FREQUENCY = ['5m', '15m', '30m', '1h', 'days', 'week', 'mon', 'ex_1m', '1m', 'day', '3mon', 'year']


# FREQUEN = [48,    16,   8,     4,     1,     "1/5",  "1/30", "ex_1m", 240, "1",   "1/90", "1/365"]
# FREQUENCY = ["5m", "15m", "30m", "1h", "days", "week", "mon", "ex_1m", "1m", "day", "3mon", "year"]


def get_frequency(frequency) -> int:
    # FREQUENCY = ['5m', '15m', '30m', '1h', 'day', 'week', 'mon', '1m', '1m', 'day', '3mon', 'year']

    if isinstance(frequency, str):
        normalized = frequency.strip().lower()
        aliases = {'daily': 'day', '1d': 'day', 'monthly': 'mon', 'weekly': 'week'}
        normalized = aliases.get(normalized, normalized)
        try:
            return FREQUENCY.index(normalized)
        except ValueError as exc:
            raise ValueError(f'不支持的行情周期: {frequency!r}') from exc
    if isinstance(frequency, int) and not isinstance(frequency, bool) and 0 <= frequency < len(FREQUENCY):
        return frequency
    raise ValueError(f'行情周期必须是 0..{len(FREQUENCY) - 1} 的整数或有效名称')


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

    r = httpx.get(url, params=params, timeout=_DEFAULT_TIMEOUT)
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
