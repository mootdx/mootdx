# -*- coding: utf-8 -*-
import json
import logging
import math
import os

from pandas.core.frame import DataFrame
from pytdx.exhq import TdxExHq_API
from pytdx.hq import TdxHq_API
from tqdm import tqdm

from mootdx.utils import get_stock_market, get_stock_markets

logger = logging.getLogger(__name__)


# 股票市场
class Quotes(object):
    @staticmethod
    def factory(market='std', **kwargs):
        if market == 'ext':
            return ExtQuotes(**kwargs)
        elif market == 'std':
            return StdQuotes(**kwargs)

    # 财务数据下载 affairs
    @staticmethod
    def financial(downdir='.'):
        from pytdx.crawler.base_crawler import demo_reporthook
        from pytdx.crawler.history_financial_crawler import HistoryFinancialCrawler
        from pytdx.crawler.history_financial_crawler import HistoryFinancialListCrawler

        crawler = HistoryFinancialListCrawler()
        datacrawler = HistoryFinancialCrawler()
        list_data = crawler.fetch_and_parse()

        for x in tqdm(list_data):
            downfile = os.path.join(downdir, x['filename'])
            result = datacrawler.fetch_and_parse(reporthook=demo_reporthook, filename=x['filename'],
                                                 path_to_download=downfile)


class StdQuotes(object):
    """股票市场实时行情"""

    # def __del__(self):
    #     if self.client:
    #         self.client.disconnect()

    # __slots__ =
    def __init__(self, **kwargs):
        self.config = None
        self.client = None

        try:
            self.config = json.loads(os.path.join(os.environ['HOME'], '.mootdx/config.josn'))
        except Exception as e:
            self.config = None

        self.client = TdxHq_API(**kwargs)

        if not self.config:
            self.bestip = os.environ.setdefault("MOOTDX_SERVER", '202.108.253.131:7709')
            self.bestip = self.bestip.split(':')
            self.bestip[1] = int(self.bestip[1])
        else:
            self.bestip = self.config.get('SERVER')

    def traffic(self):
        with self.client.connect(*self.bestip):
            return self.client.get_traffic_stats()

    # quotes
    def quotes(self, symbol=[]):
        '''
        获取实时日行情数据

        :param symbol: 股票代码
        :return: pd.dataFrame or None
        '''

        logger.debug(type(logger))

        if type(symbol) is str:
            symbol = [symbol]

        with self.client.connect(*self.bestip):
            symbol = get_stock_markets(symbol)
            result = self.client.get_security_quotes(symbol)

            if result:
                return self.client.to_df(result)

        return None

    # K线
    def bars(self, symbol='000001', category='9', start='0', offset='100'):
        '''
        获取实时日K线数据

        :param symbol: 股票代码
        :param category: 数据类别
        :param market: 证券市场
        :param start: 开始位置
        :param offset: 每次获取条数
        :return: pd.dataFrame or None
        '''
        with self.client.connect(*self.bestip):
            market = get_stock_market(symbol)
            result = self.client.get_security_bars(
                int(category), int(market), str(symbol), int(start), int(offset))

            if result:
                return self.client.to_df(result)

        return None

    # 分时数据
    def minute(self, symbol=''):
        '''
        获取实时分时数据

        :param market: 证券市场
        :param symbol: 股票代码
        :return: pd.DataFrame
        '''
        with self.client.connect(*self.bestip):
            market = get_stock_market(symbol)
            result = self.client.get_minute_time_data(int(market), symbol)

            if result:
                return self.client.to_df(result)

        return result

    # 分时历史数据
    def minute_his(self, symbol='', datetime='20191023'):
        '''
        分时历史数据

        :param market:
        :param symbol:
        :param datetime:
        :return: pd.dataFrame or None
        '''
        with self.client.connect(*self.bestip):
            market = get_stock_market(symbol)
            result = self.client.get_history_minute_time_data(
                int(market), symbol, datetime)

            if result:
                return self.client.to_df(result)

        return None

    def transaction(self, symbol='', start=0, offset=10):
        '''
        查询分笔成交

        :param market: 市场代码
        :param symbol: 股票代码
        :param start: 起始位置
        :param offset: 请求数量
        :return: pd.dataFrame or None
        '''
        with self.client.connect(*self.bestip):
            market = get_stock_market(symbol)
            result = self.client.get_transaction_data(
                int(market), symbol, int(start), int(market))

            if result:
                return self.client.to_df(result)

        return None

    def transactions(self, symbol='', start=0, offset=10, date='20170209'):
        '''
        查询历史分笔成交
        参数：市场代码， 股票代码，起始位置，日期 数量 如： 0,000001,0,10,20170209


        :param market: 市场代码
        :param symbol: 股票代码
        :param start: 起始位置
        :param offset: 数量
        :param date: 日期
        :return: pd.dataFrame or None
        '''
        with self.client.connect(*self.bestip):
            market = get_stock_market(symbol, string=True)
            market = 0 if market == 'sz' else 1
            result = self.client.get_history_transaction_data(
                int(market), symbol, int(start), int(offset), date)

            if isinstance(result, DataFrame):
                if len(result):
                    return result
            else:
                return self.client.to_df(result)

        return None

    def company(self, symbol='', detail='category', *args, **kwargs):
        '''
        企业信息获取

        :param symbol:
        :param detail:
        :param args:
        :param kwargs:
        :return:
        '''
        pass

    def F10C(self, symbol=''):
        '''
        查询公司信息目录

        :param market: 市场代码
        :param symbol: 股票代码
        :return: pd.dataFrame or None
        '''
        with self.client.connect(*self.bestip):
            market = get_stock_market(symbol)
            result = self.client.get_company_info_category(int(market), symbol)

            if result:
                return self.client.to_df(result)

        return None

    def F10(self, symbol='', file='', start=0, offset=10):
        '''
        读取公司信息详情

        :param market: 市场代码
        :param symbol: 股票代码
        :param file: 文件名
        :param start: 起始位置
        :param offset: 数量
        :return: pd.dataFrame or None
        '''
        with self.client.connect(*self.bestip):
            market = get_stock_market(symbol, string=True)
            market = 0 if market == 'sz' else 1
            result = self.client.get_company_info_content(
                int(market), symbol, file, int(start), int(offset))

            if result:
                return self.client.to_df(result)

        return None

    def xdxr(self, symbol=''):
        '''
        读取除权除息信息

        :param market: 市场代码
        :param symbol: 股票代码
        :return: pd.dataFrame or None
        '''
        with self.client.connect(*self.bestip):
            market = get_stock_market(symbol)
            result = self.client.get_xdxr_info(int(market), symbol)

            if result:
                self.client.to_df(result)

        return result

    def k(self, symbol='', begin=None, end=None):
        '''
        读取k线信息

        :param symbol:
        :param begin: 开始日期
        :param end: 截止日期
        :return: pd.dataFrame or None
        '''
        with self.client.connect(*self.bestip):
            result = self.client.get_k_data(symbol, begin, end)

            if isinstance(result, DataFrame):
                if len(result):
                    return result

                return self.client.to_df(result)

        return None

    def index(
        self,
        symbol='000001',
        market='sh',
        category='9',
        start=1,
        offset=2):
        '''
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
        :param category: 数据类别
        :param market: 证券市场
        :param start: 开始位置
        :param offset: 每次获取条数
        :return: pd.dataFrame or None
        '''
        with self.client.connect(*self.bestip):
            market = 1 if market == 'sz' else 0
            result = self.client.get_index_bars(
                int(category), int(market), str(symbol), int(start), int(offset))

            if result:
                return self.client.to_df(result)

        return None

    def block(self, tofile="block.dat"):
        '''
        获取证券板块信息

        :param tofile:
        :return: pd.dataFrame or None
        '''
        with self.client.connect(*self.bestip):
            result = self.client.get_and_parse_block_info(tofile)

            if result:
                return self.client.to_df(result)

        return None

    def batch(self, method='', offset=100, *args, **kwargs):
        '''
        批量下载相关数据

        :param method:
        :param offset:
        :return:
        '''

        pass


class ExtQuotes(object):
    """扩展市场实时行情"""

    def __del__(self):
        if self.client:
            self.client.disconnect()

    def __init__(self, **kwargs):
        self.client = TdxExHq_API(**kwargs)
        # self.bestip = os.environ.setdefault("MOOTDX_SERVER", '61.152.107.141:7727')
        # self.bestip = kwargs.get("bestip", '202.108.253.131:7709')
        # self.bestip = self.bestip.split(':')
        self.bestip = ('112.74.214.43', 7727)
        # self.client = self.client.connect(*self.bestip)
        # self.bestip[1] = int(self.bestip[1])

    # def connect(self):
    #     if not self.client:
    #         self.client = self.connect(*self.bestip)

    def markets(self):
        '''
        获取实时市场列表

        :return: pd.dataFrame or None
        '''
        with self.client.connect(*self.bestip) as client:
            data = client.get_markets()

            if data:
                return self.client.to_df(data)

        return None

    # 查询代码列表
    def instrument(self, begin=0, end=100):
        with self.client.connect(*self.bestip):
            data = self.client.get_instrument_info(0, 100)

            if data:
                return self.client.to_df(data)

        return None

        # 查询市场中商品数量

    def instruments(self):
        with self.client.connect(*self.bestip):
            count = self.client.get_instrument_count()
            pages = math.ceil(count / 100)
            datas = []

            for page in tqdm(range(0, pages)):
                datas += self.client.get_instrument_info(page * 100, (page + 1) * 100)

            return self.client.to_df(datas)

    # 查询五档行情
    def quote(self, market='', symbol=''):
        with self.client.connect(*self.bestip):
            result = self.client.get_instrument_quote(market, symbol)

            if isinstance(result, DataFrame):
                if len(result):
                    return result
            else:
                return self.client.to_df(result)

        return None

    # 查询分时行情
    def minute(self, market='', symbol=''):
        with self.client.connect(*self.bestip):
            result = self.client.get_minute_time_data(market, symbol)

            if isinstance(result, DataFrame):
                if len(result):
                    return result
            else:
                return self.client.to_df(result)

        return None

    # 查询历史分时行情
    def minutes(self, market='', symbol='', date=''):
        with self.client.connect(*self.bestip):
            result = self.client.get_history_minute_time_data(market, symbol, date)

            if isinstance(result, DataFrame):
                if len(result):
                    return result
            else:
                return self.client.to_df(result)

        return None

    # 查询k线数据
    # 参数： K线周期， 市场ID， 证券代码，起始位置， 数量
    def bars(self, category='', market='', symbol='', begin='', num=0):
        with self.client.connect(*self.bestip):
            result = self.client.get_instrument_bars(category, market, symbol, begin, num)

            if isinstance(result, DataFrame):
                if len(result):
                    return result
            else:
                return self.client.to_df(result)

        return None

    # 查询分笔成交
    def transaction(self, market='', symbol=''):
        with self.client.connect(*self.bestip):
            result = self.client.get_transaction_data(market, symbol)

            if isinstance(result, DataFrame):
                if len(result):
                    return result
            else:
                return self.client.to_df(result)

        return None

    # 查询历史分笔成交
    def transactions(self, market=31, symbol='', date='20170810'):
        with self.client.connect(*self.bestip):
            result = self.client.get_history_transaction_data(market, symbol, date)

            if isinstance(result, DataFrame):
                if len(result):
                    return result
            else:
                return self.client.to_df(result)

        return None
