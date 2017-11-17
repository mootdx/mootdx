# -*- coding: utf-8 -*-
from pytdx.exhq import TdxExHq_API
from pytdx.hq import TdxHq_API


class LiveBars(object):
    """股票市场实时行情"""

    def __init__(self, **kwargs):
        self.client = TdxHq_API(**kwargs)

    # K线
    def bars(self, symbol='000001', category='9', market='0', start='0', offset='100'):
        '''
        获取实时日K线数据

        :param symbol: 股票代码
        :param category: 数据类别
        :param market: 证券市场
        :param start: 开始位置
        :param offset: 每次获取条数
        :return: pd.dataFrame or None
        '''
        with self.client.connect():
            data = self.client.get_security_bars(int(category), int(market), str(symbol), int(start), int(offset))
            return self.client.to_df(data)

    # 分时数据
    def minute(self, market='1', symbol=''):
        '''
        获取实时分时数据

        :param market: 证券市场
        :param symbol: 股票代码
        :return: pd.DataFrame
        '''
        with self.client.connect():
            data = self.client.get_minute_time_data(int(market), symbol)
            return self.client.to_df(data)

    # 分时历史数据
    def minute_his(self, market='1', symbol='', datetime='20161209'):
        '''
        分时历史数据

        :param market:
        :param symbol:
        :param datetime:
        :return: pd.dataFrame or None
        '''
        with self.client.connect():
            data = self.client.get_history_minute_time_data(int(market), symbol, datetime)
            return self.client.to_df(data)

    def trans(self, market='1', symbol='', start='', offset=10):
        '''

        :param market:
        :param symbol:
        :param start:
        :param offset:
        :return: pd.dataFrame or None
        '''
        with self.client.connect():
            data = self.client.get_transaction_data(int(market), symbol, int(start), int(market))
            return self.client.to_df(data)

    def trans_his(self, market=1, symbol='', start=0, offset=10, date=''):
        '''

        :param market:
        :param symbol:
        :param start:
        :param offset:
        :param date:
        :return: pd.dataFrame or None
        '''
        with self.client.connect():
            data = self.client.get_history_transaction_data(int(market), symbol, int(start), int(offset), date)
            return self.client.to_df(data)

    def company_category(self, market='1', symbol=''):
        '''
        获取公司分立

        :param market:
        :param symbol:
        :return: pd.dataFrame or None
        '''
        with self.client.connect():
            data = self.client.get_company_info_category(int(market), symbol)
            return self.client.to_df(data)

    def company_content(self, market='1', symbol='', file='', start='', offset=10):
        '''
        获取公司信息

        :param market:
        :param symbol:
        :param file:
        :param start:
        :param offset:
        :return: pd.dataFrame or None
        '''
        with self.client.connect():
            data = self.client.get_company_info_content(int(market), symbol, file, int(start), int(offset))
            return self.client.to_df(data)

    def finance(self, market='1', symbol=''):
        '''
        获取金融信息

        :param market:
        :param symbol:
        :return: pd.dataFrame or None
        '''
        with self.client.connect():
            data = self.client.get_finance_info(int(market), symbol)
            return self.client.to_df(data)

    def k(self, symbol='', start='', offset=10):
        '''

        :param symbol:
        :param start:
        :param offset:
        :return: pd.dataFrame or None
        '''
        with self.client.connect():
            data = self.client.get_k_data(symbol, int(start), int(offset))
            return self.client.to_df(data)

    def block(self, tofile="block.dat"):
        '''
        获取证券板块信息

        :param tofile:
        :return: pd.dataFrame or None
        '''
        with self.client.connect():
            data = self.client.get_and_parse_block_info(tofile)
            return self.client.to_df(data)


class ExLiveBars(LiveBars):
    """扩展市场实时行情"""

    def __init__(self, **kwargs):
        self.client = TdxExHq_API(**kwargs)

    def bars(self, symbol='', category='1', market='0', start='0', offset='100'):
        '''
        获取实时日K线数据

        :param symbol:
        :param category:
        :param market:
        :param start:
        :param offset:
        :return: pd.dataFrame or None
        '''
        with self.client.connect():
            data = self.client.get_security_bars(int(category), int(market), str(symbol), int(start), int(offset))
            return self.client.to_df(data)

    def markets(self):
        '''
        获取实时市场列表

        :return: pd.dataFrame or None
        '''
        with self.client.connect():
            data = self.client.get_markets()
            return self.client.to_df(data)

    def instrument(self, start=0, offset=100):
        '''

        :param start:
        :param offset:
        :return: pd.dataFrame or None
        '''
        with self.client.connect():
            data = self.client.get_instrument_info(int(start), int(offset))
            return self.client.to_df(data)
