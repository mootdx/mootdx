# -*- coding: utf-8 -*-
import os

from mootdx.utils import get_stock_market
from pytdx.exhq import TdxExHq_API
from pytdx.hq import TdxHq_API


# 股票市场
class Quotes(object):
    @staticmethod
    def factory(market='std', **kwargs):
        if market=='ext':
            return ExtQuotes(**kwargs)
        elif market=='std':
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
            result = datacrawler.fetch_and_parse(reporthook=demo_reporthook, filename=x['filename'], path_to_download=downfile)


class StdQuotes(object):
    """股票市场实时行情"""

    # __slots__ =
    def __init__(self, **kwargs):
        self.client = TdxHq_API(**kwargs)
        self.bestip = os.environ.setdefault("MOOTDX_SERVER", '202.108.253.131:7709')
        # self.bestip = kwargs.get("bestip", '202.108.253.131:7709')
        self.bestip = self.bestip.split(':')
        self.bestip[1] = int(self.bestip[1])

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
        market = get_stock_market(symbol)

        with self.client.connect(*self.bestip):
            data = self.client.get_security_bars(
                int(category), int(market), str(symbol), int(start), int(offset))
            return self.client.to_df(data)

    # 分时数据
    def minute(self, symbol=''):
        '''
        获取实时分时数据

        :param market: 证券市场
        :param symbol: 股票代码
        :return: pd.DataFrame
        '''
        market = get_stock_market(symbol)

        with self.client.connect(*self.bestip):
            data = self.client.get_minute_time_data(int(market), symbol)
            return self.client.to_df(data)

    # 分时历史数据
    def minute_his(self, symbol='', datetime='20161209'):
        '''
        分时历史数据

        :param market:
        :param symbol:
        :param datetime:
        :return: pd.dataFrame or None
        '''
        market = get_stock_market(symbol)

        with self.client.connect(*self.bestip):
            data = self.client.get_history_minute_time_data(
                int(market), symbol, datetime)
            return self.client.to_df(data)

    def trans(self, symbol='', start=0, offset=10):
        '''
        查询分笔成交

        :param market: 市场代码
        :param symbol: 股票代码
        :param start: 起始位置
        :param offset: 请求数量
        :return: pd.dataFrame or None
        '''
        market = get_stock_market(symbol)

        with self.client.connect(*self.bestip):
            data = self.client.get_transaction_data(
                int(market), symbol, int(start), int(market))
            return self.client.to_df(data)

    def trans_his(self, symbol='', start=0, offset=10, date=''):
        '''
        查询历史分笔成交

        :param market: 市场代码
        :param symbol: 股票代码
        :param start: 起始位置
        :param offset: 数量
        :param date: 日期
        :return: pd.dataFrame or None
        '''
        market = get_stock_market(symbol)

        with self.client.connect(*self.bestip):
            data = self.client.get_history_transaction_data(
                int(market), symbol, int(start), int(offset), date)
            return self.client.to_df(data)

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

    def company_category(self, symbol=''):
        '''
        查询公司信息目录

        :param market: 市场代码
        :param symbol: 股票代码
        :return: pd.dataFrame or None
        '''
        market = get_stock_market(symbol)

        with self.client.connect(*self.bestip):
            data = self.client.get_company_info_category(int(market), symbol)
            return self.client.to_df(data)

    def company_content(self, symbol='', file='', start=0, offset=10):
        '''
        读取公司信息详情

        :param market: 市场代码
        :param symbol: 股票代码
        :param file: 文件名
        :param start: 起始位置
        :param offset: 数量
        :return: pd.dataFrame or None
        '''
        market = get_stock_market(symbol)

        with self.client.connect(*self.bestip):
            data = self.client.get_company_info_content(
                int(market), symbol, file, int(start), int(offset))
            return self.client.to_df(data)

    def xdxr(self, symbol=''):
        '''
        读取除权除息信息

        :param market: 市场代码
        :param symbol: 股票代码
        :return: pd.dataFrame or None
        '''
        market = get_stock_market(symbol)

        with self.client.connect(*self.bestip):
            data = self.client.get_xdxr_info(int(market), symbol)
            return self.client.to_df(data)

    def k(self, symbol='', begin=None, end=None):
        '''
        读取k线信息

        :param symbol:
        :param begin:
        :param end:
        :return: pd.dataFrame or None
        '''
        with self.client.connect(*self.bestip):
            data = self.client.get_k_data(symbol, begin, end)
            return data

    def index(
        self,
        symbol='000001',
        market='sh',
        category='9',
        start='0',
        offset='100'):
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
        market = 1 if market == 'sh' else 0

        with self.client.connect(*self.bestip):
            data = self.client.get_index_bars(
                int(category), int(market), str(symbol), int(start), int(offset))
            return self.client.to_df(data)

    def block(self, tofile="block.dat"):
        '''
        获取证券板块信息

        :param tofile:
        :return: pd.dataFrame or None
        '''
        with self.client.connect(*self.bestip):
            data = self.client.get_and_parse_block_info(tofile)
            return self.client.to_df(data)

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

    def __init__(self, **kwargs):
        self.client = TdxExHq_API(**kwargs)
        # self.bestip = os.environ.setdefault("MOOTDX_SERVER", '61.152.107.141:7727')
        # self.bestip = kwargs.get("bestip", '202.108.253.131:7709')
        # self.bestip = self.bestip.split(':')
        self.bestip = ('61.152.107.141', 7727)
        # self.bestip[1] = int(self.bestip[1])

    def markets(self):
        '''
        获取实时市场列表

        :return: pd.dataFrame or None
        '''
        with self.client.connect(*self.bestip):
            data = self.client.get_markets()
            return self.client.to_df(data)

    def quote5(self, market=47, symbol="IF1709"):
        '''
        查询五档行情

        :return: pd.dataFrame or None
        '''
        with self.client.connect(*self.bestip):
            data = self.client.get_instrument_quote(market, symbol)
            return self.client.to_df(data)


    def minute(self, market=47, symbol="IF1709"):
        '''
        查询五档行情

        :return: pd.dataFrame or None
        '''
        with self.client.connect(*self.bestip):
            data = self.client.get_minute_time_data(market, symbol)
            return self.client.to_df(data)

    def instrument(self, start=0, offset=100):
        '''
        查询代码列表
        :param start:
        :param offset:
        :return: pd.dataFrame or None
        '''
        with self.client.connect(*self.bestip):
            # nums = self.client.get_instrument_count()
            data = self.client.get_instrument_info(int(start), int(offset))
            return self.client.to_df(data)
