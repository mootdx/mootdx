# -*- coding: utf-8 -*-
import unittest

from mootdx.quotes import Quotes


class TestStdQuotes(unittest.TestCase):
    client = None

    # 初始化工作
    def setUp(self):
        self.client = Quotes.factory(market='std')  # 标准市场

    # 退出清理工作
    def tearDown(self):
        self.client = None

    # def test_transaction(self):
    #     result = self.client.transaction(symbol='600036', start=0, offset=10)
    #     self.assertIsNotNone(result)
    #
    # def test_transactions(self):
    #     result = self.client.transactions(symbol='000001', start=0, offset=10, date='20191025')
    #     self.assertIsNotNone(result)

    def test_F10(self):
        # data = self.client.F10C(symbol='000001')
        data = self.client.F10(symbol='000001', file='000001.txt', start=0, offset=100)
        self.assertIsNotNone(data)
