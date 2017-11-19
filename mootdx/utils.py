import datetime
import io
import re
import time
from datetime import datetime, timedelta
from functools import lru_cache

import pandas as pd
import requests
from pytdx.config.hosts import hq_hosts as hosts
from pytdx.exhq import TdxExHq_API
from pytdx.hq import TdxHq_API


def ping(ip):
    api = TdxHq_API()
    now = datetime.now()

    try:
        with api.connect(ip[1], int(ip[2])):
            if len(api.get_security_list(0, 1)) > 800:
                return datetime.now() - now
    except:
        print('Bad REPSONSE %s' % ip[1])
        return timedelta(9, 9, 0)


def best_ip():
    print('Selecting the Best Server IP of TDX')
    data = [ping(x) for x in hosts]
    print('===The BEST SERVER is :  %s ===' % (hosts[data.index(min(data))]))
    return hosts[data.index(min(data))]


def get_index_market(symbol=''):
    pass

def get_stock_market(symbol=''):
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
    
    return 1 if market == 'sz' else 0


def get_code_type(code):
    """
    判断代码是属于那种类型，目前仅支持 ['fund', 'stock']
    :return str 返回code类型, fund 基金 stock 股票
    """
    if code.startswith(('00', '30', '60')):
        return 'stock'

    return 'fund'


def round_price_by_code(price, code):
    """
    根据代码类型[股票，基金] 截取制定位数的价格
    :param price: 证券价格
    :param code: 证券代码
    :return: str 截断后的价格的字符串表示
    """
    if isinstance(price, str):
        return price

    typ = get_code_type(code)

    if typ == 'fund':
        return '{:.3f}'.format(price)

    return '{:.2f}'.format(price)


def get_ipo_info(only_today=False):
    import pyquery

    response = requests.get('http://vip.stock.finance.sina.com.cn/corp/go.php/vRPD_NewStockIssue/page/1.phtml', headers={'accept-encoding': 'gzip, deflate, sdch'})
    html = response.content.decode('gbk')

    html_obj = pyquery.PyQuery(html)
    table_html = html_obj('#con02-0').html()

    df = pd.read_html(io.StringIO(table_html), skiprows=3, converters={
        '证券代码': str,
        '申购代码': str}
    )[0]

    if only_today:
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        df = df[df['上网发行日期↓'] == today]

    return df

@lru_cache()
def is_holiday(day):
    """
    判断是否节假日, api 来自百度 apistore: http://apistore.baidu.com/apiworks/servicedetail/1116.html
    :param day: 日期， 格式为 '20160404'
    :return: bool
    """
    api = 'http://tool.bitefu.net/jiari/'
    params = {'d': day, 'apiserviceid': 1116}

    rep = requests.get(api, params)
    res = rep.text

    return True if res != "0" else False


def is_holiday_today():
    """
    判断今天是否时节假日
    :return: bool
    """
    today = datetime.date.today().strftime('%Y%m%d')
    return is_holiday(today)


def is_tradetime_now():
    """
    判断目前是不是交易时间, 并没有对节假日做处理
    :return: bool
    """
    now_time = time.localtime()
    now = (now_time.tm_hour, now_time.tm_min, now_time.tm_sec)
    
    if (9, 15, 0) <= now <= (11, 30, 0) or (13, 0, 0) <= now <= (15, 0, 0):
        return True

    return False


def calc_next_trade_time_delta_seconds():
    now_time = datetime.datetime.now()
    now = (now_time.hour, now_time.minute, now_time.second)

    if now < (9, 15, 0):
        next_trade_start = now_time.replace(hour=9, minute=15, second=0, microsecond=0)
    elif (12, 0, 0) < now < (13, 0, 0):
        next_trade_start = now_time.replace(hour=13, minute=0, second=0, microsecond=0)
    elif now > (15, 0, 0):
        distance_next_work_day = 1
        while True:
            target_day = now_time + timedelta(days=distance_next_work_day)
            if is_holiday(target_day.strftime('%Y%m%d')):
                distance_next_work_day += 1
            else:
                break

        day_delta = timedelta(days=distance_next_work_day)
        next_trade_start = (now_time + day_delta).replace(hour=9, minute=15,
                                                          second=0, microsecond=0)
    else:
        return 0

    time_delta = next_trade_start - now_time
    return time_delta.total_seconds()
