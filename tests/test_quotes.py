# -*- coding: utf-8 -*-
import unittest

from mootdx.quotes import Quotes


class TestStdQuotes(unittest.TestCase):
    reader = None

    # 初始化工作
    def setUp(self):
        self.client = Quotes.factory(market='std', multithread=True, heartbeat=True) # 标准市场

    # 退出清理工作
    def tearDown(self):
        del self.client

    # 具体的测试用例，一定要以test开头
    def test_bars(self):
        data = self.client.bars(symbol='600036', category=9, offset=10)
        self.assertTrue(data is not None)

    def test_index(self):
        data = self.client.index(symbol='000001', category=9)
        self.assertTrue(data is not None)

    def test_minute(self):
        data = self.client.minute(symbol='000001')
        self.assertTrue(data is not None)

    def test_minutes(self):
        data = self.client.minute_his(symbol='000001', datetime='20171010')
        self.assertTrue(data is not None)

    def test_trans(self):
        data = self.client.trans(symbol='600036', start=0, offset=10)
        self.assertTrue(data is not None)

    def test_trans_his(self):
        data = self.client.trans_his(symbol='600036', start=0, offset=10, date='20171010')
        self.assertTrue(data is not None)

    def test_company_category(self):
        data = self.client.company_category(symbol='600036')
        self.assertTrue(data is not None)

    def test_company_content(self):
        data = self.client.company_content(symbol='600036', file='600036.txt', start=9442, offset=11863)
        self.assertTrue(data is not None)

    def test_xdxr(self):
        data = self.client.xdxr(symbol='600036')
        self.assertTrue(data is not None)

    def test_k(self):
        data = self.client.k(symbol='600036', begin=0, end=10)
        self.assertTrue(data is not None)

    def test_block(self):
        data = self.client.block()
        self.assertTrue(data is not None)


class TestExtQuotes(unittest.TestCase):
    reader = None

    # 初始化工作
    def setUp(self):
        self.client = Quotes.factory(market='ext', multithread=True, heartbeat=True) # 标准市场

    # 退出清理工作
    def tearDown(self):
        del self.client

    # 具体的测试用例，一定要以test开头
    def test_markets(self):
        data = self.client.markets()
        self.assertTrue(data is not None)

if __name__ == '__main__':
    unittest.main()
