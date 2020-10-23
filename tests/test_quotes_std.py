# -*- coding: utf-8 -*-
import unittest

from mootdx.quotes import Quotes
from mootdx.consts import MARKET_SH


class TestStdQuotes(unittest.TestCase):
    client = None

    # 初始化工作
    def setUp(self):
        self.client = Quotes.factory(market='std')  # 标准市场

    # 退出清理工作
    def tearDown(self):
        del self.client

    def test_quotes(self):
        data = self.client.quotes(symbol='600036')
        self.assertIsNotNone(data)

        data = self.client.quotes(symbol=['600036', '600016'])
        self.assertIsNotNone(data)

    def test_bars(self):
        data = self.client.bars(symbol='600036', frequency=9, offset=10)
        self.assertIsNotNone(data)

    def test_index(self):
        data = self.client.index(frequency=9,
                                 market=MARKET_SH,
                                 symbol='000001',
                                 start=1,
                                 offset=2)
        self.assertIsNotNone(data)

    def test_minute(self):
        data = self.client.minute(symbol='000001')
        self.assertIsNotNone(data)

    def test_minutes(self):
        data = self.client.minutes(symbol='000001', date='20171010')
        self.assertIsNotNone(data)

    def test_transaction(self):
        data = self.client.transaction(symbol='600036', start=0, offset=10)
        self.assertIsNotNone(data)

    def test_transactions(self):
        data = self.client.transactions(symbol='000001',
                                        start=0,
                                        offset=10,
                                        date='20170209')
        self.assertIsNotNone(data)

    def test_F10C(self):
        data = self.client.F10C(symbol='000001')
        self.assertIsNotNone(data)

    def test_F10(self):
        data = self.client.F10(symbol='000001', name='龙虎榜单')
        self.assertIsNotNone(data)

    def test_xdxr(self):
        data = self.client.xdxr(symbol='600036')
        self.assertIsNotNone(data)

    def test_k(self):
        data = self.client.k(symbol='000001',
                             begin='2019-07-03',
                             end='2019-07-10')
        self.assertIsNotNone(data)

    def test_block(self):
        data = self.client.block()
        self.assertIsNotNone(data)

    def test_finance(self):
        data = self.client.finance(symbol='000001')
        self.assertIsNotNone(data)
