# -*- coding: utf-8 -*-
import contextlib
import math

import pandas
from pytdx.exhq import TdxExHq_API
from pytdx.hq import TdxHq_API
from tqdm import tqdm
from unipath import Path

from mootdx import config, server
from mootdx.consts import MARKET_SH
from mootdx.logger import log
from mootdx.utils import (get_config_path, get_stock_market, get_stock_markets, to_data)


class Quotes(object):
    @staticmethod
    def factory(market='std', **kwargs):
        """
        股票市场 工厂方法

        :param market: std 标准市场, ext 扩展市场
        :param kwargs:
        :return: object
        """
        if market == 'ext':
            return ExtQuotes(**kwargs)
        elif market == 'std':
            return StdQuotes(**kwargs)


class BaseQuotes(object):
    client = None
    bestip = None

    def __init__(self, bestip=False, timeout=15, **kwargs):
        log.debug(f'bestip=>{bestip}')

        self.timeout = timeout

        config_ = get_config_path('config.json')

        if bestip or not Path(config_).exists():
            server.bestip()

    @contextlib.contextmanager
    def connect(self):
        if self.closed:
            log.debug('服务器连接已断开，正进行重新连接...')
            self.reconnect()

        yield

        self.close()

    def __del__(self):
        log.debug('__del__')
        self.close()

    def reconnect(self):
        if self.closed:
            log.debug('服务器连接已断开，正进行重新连接...')
            self.client.connect(time_out=self.timeout, *self.bestip)

    def close(self):
        log.debug('close')
        self.client.close()

    @property
    def closed(self):
        if hasattr(self.client.client, '_closed') and not getattr(self.client.client, '_closed'):
            return False

        return True


class StdQuotes(BaseQuotes):
    """
    股票市场实时行情
    """
    bestip = ('47.103.48.45', 7709)

    def __init__(self, bestip=False, timeout=15, **kwargs):
        super(StdQuotes, self).__init__(bestip=bestip, timeout=timeout, **kwargs)

        try:
            default = config.get('SERVER').get('HQ')[0]
            self.bestip = config.get('BESTIP').get('HQ', default)
        except ValueError:
            self.bestip = ('47.103.48.45', 7709)

        self.client = TdxHq_API(**kwargs)
        self.client.connect(*self.bestip)

    def traffic(self):
        self.reconnect()
        return self.client.get_traffic_stats()

    def quotes(self, symbol=None):
        """
        获取实时日行情数据

        :param symbol: 股票代码
        :return: pd.dataFrame or None
        """

        if not symbol:
            return to_data(None)

        if type(symbol) is str:
            symbol = [symbol]

        self.reconnect()

        symbol = get_stock_markets(symbol)
        result = self.client.get_security_quotes(symbol)

        return to_data(result)

    def bars(self, symbol='000001', frequency='9', start='0', offset='100', *args, **kwargs):
        """
        获取实时日K线数据

        :param symbol: 股票代码
        :param frequency: 数据类别
        :param start: 开始位置
        :param offset: 每次获取条数
        :return: pd.dataFrame or None
        """
        self.reconnect()

        market = get_stock_market(symbol)
        result = self.client.get_security_bars(int(frequency), int(market), str(symbol), int(start), int(offset))

        return to_data(result)

    def stock_count(self, market=MARKET_SH, *args, **kwargs):
        """
        获取市场股票数量

        :param market: 股票市场代码 sh 上海， sz 深圳
        :return: pd.dataFrame or None
        """
        self.reconnect()

        result = self.client.get_security_count(market=market)

        return result

    def stocks(self, market=MARKET_SH, *args, **kwargs):
        """
        获取股票列表

        :param market: 股票市场
        :return:
        """
        self.reconnect()

        counts = self.client.get_security_count(market=market)
        stocks = None

        for start in tqdm(range(0, counts, 1000)):
            result = self.client.get_security_list(market=market, start=start)
            stocks = pandas.concat([stocks, to_data(result)], ignore_index=True) if start > 1 else to_data(result)

        return stocks

    def index_bars(self, symbol='000001', frequency='9', start='0', offset='100', *args, **kwargs):
        """
        获取指数k线

        :param symbol: 股票代码
        :param frequency:
        :param start:
        :param offset:
        :return:
        """
        self.reconnect()

        market = get_stock_market(symbol)
        result = self.client.get_index_bars(frequency=frequency, market=market, code=symbol, start=start, count=offset)

        return to_data(result)

    def minute(self, symbol=''):
        """
        获取实时分时数据

        :param symbol: 股票代码
        :return: pd.DataFrame
        """
        self.reconnect()

        market = get_stock_market(symbol)
        result = self.client.get_minute_time_data(market=market, code=symbol)

        return to_data(result)

    def minutes(self, symbol='', date='20191023', *args, **kwargs):
        """
        分时历史数据

        :param symbol: 股票代码
        :param date:
        :return: pd.dataFrame or None
        """
        self.reconnect()

        market = get_stock_market(symbol)
        result = self.client.get_history_minute_time_data(market=market, code=symbol, date=date)

        return to_data(result)

    def transaction(self, symbol='', start=0, offset=10, *args, **kwargs):
        """
        查询分笔成交

        :param symbol: 股票代码
        :param start: 起始位置
        :return: pd.dataFrame or None
        """
        self.reconnect()

        market = get_stock_market(symbol)
        result = self.client.get_transaction_data(int(market), symbol, int(start), offset)

        return to_data(result)

    def transactions(self, symbol='', start=0, offset=10, date='20170209'):
        """
        查询历史分笔成交
        参数：市场代码， 股票代码，起始位置，日期 数量 如： 0,000001,0,10,20170209

        :param symbol: 股票代码
        :param start: 起始位置
        :param offset: 数量
        :param date: 日期
        :return: pd.dataFrame or None
        """
        self.reconnect()

        market = get_stock_market(symbol, string=False)
        result = self.client.get_history_transaction_data(market=market, code=symbol, start=start, count=offset, date=int(date))

        return to_data(result)

    def F10C(self, symbol=''):
        """
        查询公司信息目录

        :param symbol: 股票代码
        :return: pd.dataFrame or None
        """
        self.reconnect()

        market = int(get_stock_market(symbol))
        result = self.client.get_company_info_category(market, symbol)

        return result

    def F10(self, symbol='', name=''):
        """
        读取公司信息详情

        :param name: 公司 F10 标题
        :param symbol: 股票代码
        :return: pd.dataFrame or None
        """
        self.reconnect()

        result = {}
        market = int(get_stock_market(symbol, string=False))

        frequency = self.client.get_company_info_category(market, symbol)

        if name:
            for x in frequency:
                if x['name'] == name:
                    return self.client.get_company_info_content(market=market, code=symbol, filename=x['filename'], start=x['start'], length=x['length'])

        for x in frequency:
            result[x['name']] = self.client.get_company_info_content(
                market=market, code=symbol, filename=x['filename'], start=x['start'], length=x['length'])

        return result

    def xdxr(self, symbol=''):
        """
        读取除权除息信息

        :param symbol: 股票代码
        :return: pd.dataFrame or None
        """
        self.reconnect()

        market = get_stock_market(symbol)
        result = self.client.get_xdxr_info(int(market), symbol)

        return to_data(result)

    def finance(self, symbol='000001'):
        """
        读取财务信息

        :param symbol: 股票代码
        :return:
        """
        self.reconnect()

        market = get_stock_market(symbol)
        result = self.client.get_finance_info(market=market, code=symbol)

        return to_data(result)

    def k(self, symbol='', begin=None, end=None):
        """
        读取k线信息

        :param symbol:
        :param begin: 开始日期
        :param end: 截止日期
        :return: pd.dataFrame or None
        """
        self.reconnect()

        result = self.client.get_k_data(symbol, begin, end)
        return result

    def index(self, symbol='000001', market=MARKET_SH, frequency='9', start=1, offset=2):
        """
        获取指数k线

        K线种类:
        - 0 5分钟K线
        - 1 15分钟K线
        - 2 30分钟K线
        - 3 1小时K线
        - 4 日K线
        - 5 周K线
        - 6 月K线

        - 7 1分钟
        - 8 1分钟K线
        - 9 日K线
        - 10 季K线
        - 11 年K线

        :param symbol: 股票代码
        :param frequency: 数据类别
        :param market: 证券市场
        :param start: 开始位置
        :param offset: 每次获取条数
        :return: pd.dataFrame or None
        """
        self.reconnect()

        result = self.client.get_index_bars(int(frequency), int(market), str(symbol), int(start), int(offset))
        return to_data(result)

    def block(self, tofile="block.dat"):
        """
        获取证券板块信息

        :param tofile:
        :return: pd.dataFrame or None
        """
        self.reconnect()

        result = self.client.get_and_parse_block_info(tofile)
        return to_data(result)


class ExtQuotes(BaseQuotes):
    """
    扩展市场实时行情
    """

    bestip = ('112.74.214.43', 7727)

    def __init__(self, bestip=False, timeout=15, **kwargs):
        super(ExtQuotes, self).__init__(bestip=bestip, timeout=timeout, **kwargs)

        try:
            default = config.get('SERVER').get('EX')[0]
            self.bestip = config.get('BESTIP').get('EX', default)
        except ValueError:
            self.bestip = ('112.74.214.43', 7727)

        log.debug(self.bestip)

        self.client = TdxExHq_API(**kwargs)
        self.client.connect(*self.bestip)

    @staticmethod
    def validate(market, symbol):
        if not market:
            if len(symbol.split('#')) > 1:
                market = symbol.split('#')[0]
                symbol = symbol.split('#')[1]

        if not market:
            raise ValueError('市场参数错误, 市场参数不能为空.')

        return int(market), symbol

    def markets(self):
        """
        获取实时市场列表

        :return: pd.dataFrame or None
        """
        self.reconnect()

        result = self.client.get_markets()
        return to_data(result)

    def instrument(self, start=0, offset=100):
        """
        查询代码列表

        :param offset:
        :param start:
        :return:
        """
        self.reconnect()

        result = self.client.get_instrument_info(start=start, count=offset)
        return to_data(result)

    def instrument_count(self):
        """
        市场商品数量

        :return:
        """
        self.reconnect()

        result = self.client.get_instrument_count()

        return result

    def instruments(self):
        """
        查询所有代码列表

        :return:
        """
        self.reconnect()

        result = []

        count = self.client.get_instrument_count()
        pages = math.ceil(count / 100)

        for page in tqdm(range(0, pages)):
            result += self.client.get_instrument_info(page * 100, 100)

        return to_data(result)

    def quote(self, market='', symbol=''):
        """
        查询五档行情

        :param market: 市场ID
        :param symbol: 证券代码
        :return:
        """
        self.reconnect()

        market, symbol = self.validate(market, symbol)
        result = self.client.get_instrument_quote(market, symbol)

        return to_data(result)

    def minute(self, market='', symbol=''):
        """
        查询分时行情

        :param market: 市场ID
        :param symbol: 证券代码
        :return:
        """
        self.reconnect()

        market, symbol = self.validate(market, symbol)
        result = self.client.get_minute_time_data(market, symbol)

        return to_data(result)

    def minutes(self, market=None, symbol='', date=''):
        """
        查询历史分时行情

        :param market: 市场ID
        :param symbol: 证券代码
        :param date:
        :return:
        """
        self.reconnect()

        market, symbol = self.validate(market, symbol)
        result = self.client.get_history_minute_time_data(market, symbol, date)

        return to_data(result)

    def bars(self, frequency='', market='', symbol='', start=0, offset=100):
        """
        查询k线数据
        参数： K线周期， 市场ID， 证券代码，起始位置， 数量

        :param frequency: K线周期
        :param market: 市场ID
        :param symbol: 证券代码
        :param start: 起始位置
        :param offset: 数量
        :return:
        """
        self.reconnect()

        market, symbol = self.validate(market, symbol)
        result = self.client.get_instrument_bars(category=frequency, market=market, code=symbol, start=start, count=offset)

        return to_data(result)

    def transaction(self, market=None, symbol='', start=0, offset=1800):
        """
        查询分笔成交

        :param market: 市场ID
        :param symbol: 证券代码
        :param start:
        :param offset:
        :return:
        """
        self.reconnect()

        market, symbol = self.validate(market, symbol)
        result = self.client.get_transaction_data(market=market, code=symbol, start=start, count=offset)

        return to_data(result)

    def transactions(self, market=None, symbol='', date='', start=0, offset=1800):
        """
        查询历史分笔成交

        :param market: 市场ID
        :param symbol: 证券代码
        :param date:
        :param start:
        :param offset:
        :return:
        """
        self.reconnect()

        market, symbol = self.validate(market, symbol)
        result = self.client.get_history_transaction_data(market=market, code=symbol, date=int(date), start=start, count=offset)

        return to_data(result)
