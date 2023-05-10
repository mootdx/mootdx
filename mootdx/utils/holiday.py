# @Author  : BoPo
# @Time    : 2021/10/9 10:56
# @Function:
import datetime
import logging
import re
import warnings
from pathlib import Path

import httpx
import pandas as pd
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_fixed

from mootdx import get_config_path
from mootdx.cache import file_cache
from mootdx.consts import return_last_value
from mootdx.logger import logger

JS_DECODE = (Path(__file__).parent / 'holiday.js').read_text(encoding='utf-8')


@file_cache(filepath=get_config_path('holidays.plk'), refresh_time=3600 * 24)
@retry(wait=wait_fixed(2), retry_error_callback=return_last_value, stop=stop_after_attempt(5))
def holidays() -> pd.DataFrame:
    try:
        from py_mini_racer import py_mini_racer
    except (ImportError, ModuleNotFoundError):
        warnings.warn('!!! 缺少依赖, 请使用次命令进行安装: pip install py_mini_racer', DeprecationWarning)
        logging.warning('!!! 缺少依赖, 请使用次命令进行安装: pip install py_mini_racer')
        return pd.DataFrame([])

    logger.debug('调用远程接口')
    client = httpx.Client(verify=False)

    url = 'https://finance.sina.com.cn/realstock/company/klc_td_sh.txt'
    res = client.get(url)

    js_code = py_mini_racer.MiniRacer()
    js_code.eval(JS_DECODE)

    # 执行js解密代码
    dict_list = js_code.call('d', res.text.split('=')[1].split(';')[0].replace('"', ''))

    temp_df = pd.DataFrame(dict_list)
    temp_df.columns = ['date']
    temp_df['date'] = pd.to_datetime(temp_df['date']).dt.date

    temp_list = temp_df['date'].to_list()
    temp_list.append(datetime.date(1992, 5, 4))  # 是交易日但是交易日历缺失该日期
    temp_list.sort()

    temp_df = pd.DataFrame(temp_list, columns=['date'])
    temp_df['year'] = pd.DatetimeIndex(temp_df['date']).year

    return temp_df


def holiday2(date: str = None) -> pd.DataFrame:
    """交易日历-历史数据
    :return: 交易日历
    :rtype: pandas.DataFrame
    """
    try:
        from py_mini_racer import py_mini_racer
    except (ImportError, ModuleNotFoundError):
        warnings.warn('!!! 缺少依赖, 请使用次命令进行安装: pip install py_mini_racer', DeprecationWarning)
        logging.warning('!!! 缺少依赖, 请使用次命令进行安装: pip install py_mini_racer')
        return pd.DataFrame([])

    temp_df = holidays()

    if date:
        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            date = datetime.datetime.now().date()

        return temp_df[temp_df['date'] == date]

    # print(temp_df)
    return temp_df


def holiday(date=None, format_=None, country=None, result=False):
    format_ = format_ if format_ else '%Y-%m-%d'
    country = country if country else '中国'

    try:
        if date:
            date = datetime.datetime.strptime(date, format_).date()
        else:
            date = datetime.datetime.now().date()
    except ValueError as ex:
        logger.error('日期或者日期格式错误!')
        return None

    df = _holiday()

    if country not in list(set(df['国家'].values)):
        logger.error(f'没有该国家`{country}`的交易日数据')
        return None

    df = df[df['国家'] == country]
    df = df[df.index.isin([date])]

    logger.debug(date)

    if result:
        return df

    logger.debug(date.weekday())

    return not df.empty or date.weekday() >= 5


@file_cache(filepath=get_config_path('holiday.plk'), refresh_time=3600 * 24)
def _holiday():
    logger.debug('调用远程接口')
    res = httpx.get('https://www.tdx.com.cn/url/holiday/')
    res.encoding = 'gbk'

    ret = re.findall(r'<textarea id="data" style="display:none;">([\s\w\W]+)</textarea>', res.text, re.M)[0].strip()
    day = [d.split('|')[:4] for d in ret.split('\n')]

    df = pd.DataFrame(day, columns=['日期', '节日', '国家', '交易所'], dtype=str)
    df.index = pd.to_datetime(df['日期'].astype('str'), format='%Y%m%d')

    return df


def holiday_(date=None, format_=None, country=None):
    return holiday(date=date, format_=format_, country=country, result=True)
