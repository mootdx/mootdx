# -*- coding: utf-8 -*-
import unittest

from mootdx.quotes import Quotes


class TestStdQuotes(unittest.TestCase):
    client = None

    # 初始化工作
    def setUp(self):
        self.client = Quotes.factory(market='std', multithread=True, heartbeat=True) # 标准市场

    # 退出清理工作
    def tearDown(self):
        del self.client

    def test_quotes(self):
        data = self.client.quotes(symbol='600036')
        self.assertTrue(data is not None)
        
        data = self.client.quotes(symbol=['600036', '600016'])
        self.assertTrue(data is not None)

    def test_bars(self):
        data = self.client.bars(symbol='600036', category=9, offset=10)
        self.assertTrue(data is not None)

    def test_index(self):
        data = self.client.index(category=9, market='sz', symbol='000001', start=1, offset=2)
        self.assertTrue(data is not None)

    def test_minute(self):
        data = self.client.minute(symbol='000001')
        self.assertTrue(data is not None)

    def test_minutes(self):
        data = self.client.minute_his(symbol='000001', datetime='20171010')
        self.assertTrue(data is not None)

    def test_transaction(self):
        data = self.client.transaction(symbol='600036', start=0, offset=10)
        self.assertTrue(data is not None)

    def test_transactions(self):
        # api.get_history_transaction_data(TDXParams.MARKET_SZ, '000001', 0, 10, 20170209)
        data = self.client.transactions(symbol='000001', start=0, offset=10, date='20170209')
        self.assertTrue(data is not None)

    def test_company_category(self):
        data = self.client.company_category(symbol='000001')
        self.assertTrue(data is not None)

    def test_company_content(self):
        # api.get_company_info_content(0, '000001', '000001.txt', 0, 100)                                                     # 
        data = self.client.company_content(symbol='000001', file='000001.txt', start=0, offset=100)
        self.assertTrue(data is not None)

    def test_xdxr(self):
        data = self.client.xdxr(symbol='600036')
        self.assertTrue(data is not None)

    def test_k(self):
        data = self.client.k(symbol='000001', begin='2017-07-03', end='2017-07-10')
        self.assertTrue(data is not None)

    def test_block(self):
        data = self.client.block()
        self.assertTrue(data is not None)
