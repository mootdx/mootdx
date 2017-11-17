# -*- coding: utf-8 -*-
from pytdx.hq import TdxHq_API
from pytdx.exhq import TdxExHq_API

class LiveBars(object):
    """股票市场实时行情"""

    def __init__(self, **kwargs):
        self.client = TdxHq_API()

    # K线
    def bars(self, symbol='000001', category='9', market='0', start='0', offset='100'):
        with self.client.connect():
            data = self.client.get_security_bars(int(category), int(market), str(symbol), int(start), int(offset))
            return self.client.to_df(data)
            
        return None

    # 分时数据
    def minute(self, market='1', symbol=''):
        with self.client.connect():
            data = self.client.get_minute_time_data(int(market), symbol)
            return self.client.to_df(data)

        return None

    # 分时历史数据
    def minute_his(self, market='1', symbol='', datetime='20161209'):
        with self.client.connect():
            data = self.client.get_history_minute_time_data(int(market), symbol, datetime)
            return self.client.to_df(data)

        return None

    def trans(self, market='1', symbol='', start='', offset=10):
        with self.client.connect():
            data = self.client.get_transaction_data(int(market), symbol, int(start), int(market))
            return self.client.to_df(data)

        return None

    def trans_his(self, market=1, symbol='', start=0, offset=10, date=''):
        with self.client.connect():
            data = self.client.get_history_transaction_data(int(market), symbol, int(start), int(offset), date)
            return self.client.to_df(data)
            
        return None

    def company_category(self, market='1', symbol=''):
        with self.client.connect():
            data = self.client.get_company_info_category(int(market), symbol)
            return self.client.to_df(data)
        
        return None

    def company_content(self, market='1', symbol='', file='', start='', offset=10):
        with self.client.connect():
            data = self.client.get_company_info_content(int(market), symbol, file, int(start), int(offset))
            return self.client.to_df(data)
        
        return None

    def finance(self, market='1', symbol=''):
        with self.client.connect():
            data = self.client.get_finance_info(int(market), symbol)
            return self.client.to_df(data)
        
        return None

    def k(self, symbol='', start='', offset=10):
        with self.client.connect():
            data = self.client.get_k_data(symbol, int(start), int(offset))
            return self.client.to_df(data)
    
        return None
    
    def block(self, tofile="block.dat"):
        with self.client.connect():
            data = self.client.get_and_parse_block_info(tofile)
            return self.client.to_df(data)
        
        return None

class ExLiveBars(LiveBars):
    """扩展市场实时行情"""
    def __init__(self, **kwargs):
        self.client = TdxExHq_API(auto_retry=True)

    def bars(self, symbol='', category='1', market='0', start='0', offset='100'):
        with self.client.connect():
            data = self.client.get_security_bars(int(category), int(market), str(symbol), int(start), int(offset))
            return self.client.to_df(data)
            
        return None

    def markets(self):
        with self.client.connect():
            data = self.client.get_markets()
            return self.client.to_df(data)

        return None

    def instrument(self, start=0, offset=100):
        with self.client.connect():
            data = self.client.get_instrument_info(int(start), int(offset))
            return self.client.to_df(data)
        
        return None            
        
