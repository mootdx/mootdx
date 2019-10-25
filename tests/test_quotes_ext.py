# -*- coding: utf-8 -*-
import unittest

from mootdx.quotes import Quotes


class TestExtQuotes(unittest.TestCase):
    client = None

    # 初始化工作
    def setUp(self):
        self.client = Quotes.factory(market='ext', multithread=False, heartbeat=False) 

    # 退出清理工作
    def tearDown(self):
        self.client = None

    # 具体的测试用例，一定要以test开头
    def test_markets(self):
        data = self.client.markets()
        self.assertTrue(data is not None)    

    # 具体的测试用例，一定要以test开头
    def test_instrument(self):
        data = self.client.instrument(0, 100)
        self.assertTrue(data is not None)

    # 具体的测试用例，一定要以test开头
    # def test_instruments(self):
    #     data = self.client.instruments()
    #     self.assertTrue(data is not None)

    # api.get_instrument_quote(47, "IF1709")
    def test_quote(self):
        data = self.client.quote(market=47, symbol='IF1709')
        self.assertTrue(data is not None)

    # api.get_instrument_quote(47, "IF1709")
    def test_minute(self):
        data = self.client.minute(market=47, symbol='IF1709')
        self.assertTrue(data is not None)

    def test_minutes(self):
        data = self.client.minutes(market=47, symbol='IF1709')
        self.assertTrue(data is not None)

    def test_bars(self):
        data = self.client.bars(market=47, symbol='IF1709')
        self.assertTrue(data is not None)

    def test_transactions(self):
        data = self.client.transactions(market=47, symbol='IF1709')
        self.assertTrue(data is not None)

    def test_transactions(self):
        data = self.client.transactions(market=47, symbol='IF1709')
        self.assertTrue(data is not None)
        
if __name__ == '__main__':
    unittest.main()
