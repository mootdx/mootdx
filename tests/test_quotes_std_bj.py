import unittest

import pytest

from mootdx.logger import logger
from mootdx.quotes import Quotes


class TestStdQuotes(unittest.TestCase):
    client = None

    # 初始化工作
    def setup_class(self):
        self.client = Quotes.factory(market='std', timeout=10)  # 标准市场
        logger.success('初始化工作')

    # 退出清理工作
    def teardown_class(self):
        self.client.client.close()
        del self.client
        logger.success('退出清理工作')

    def test_quotes(self):
        data = self.client.quotes(symbol='430090')
        self.assertEqual(data.empty, False)

        data = self.client.quotes(symbol='430090')
        self.assertEqual(data.empty, False)

        data = self.client.quotes(symbol=['600036', '600016'])
        self.assertEqual(data.empty, False)

    def test_bars(self):
        data = self.client.bars(symbol='430090', frequency=9, offset=10)
        self.assertEqual(data.empty, False)

    def test_minute(self):
        data = self.client.minute(symbol='430090')
        self.assertEqual(data.empty, False)

    # @todo
    @pytest.mark.skip
    def test_minutes(self):
        data = self.client.minutes(symbol='430090', date='20171010')
        self.assertEqual(data.empty, False)

    def test_transaction(self):
        data = self.client.transaction(symbol='430090', start=0, offset=10)
        self.assertEqual(data.empty, False)

    # @todo
    @pytest.mark.skip
    def test_transactions(self):
        data = self.client.transactions(symbol='430090', start=0, offset=10, date='20170209')
        self.assertEqual(data.empty, False)

    # @todo
    @pytest.mark.skip
    def test_F10C(self):
        data = self.client.F10C(symbol='430090')
        self.assertTrue(data)

    # todo
    @pytest.mark.skip
    def test_F10(self):
        data = self.client.F10(symbol='430090', name='龙虎榜单')
        self.assertTrue(data)

    def test_xdxr(self):
        data = self.client.xdxr(symbol='430090')
        self.assertEqual(data.all().empty, False)

    # @todo
    @pytest.mark.skip
    def test_k(self):
        data = self.client.k(symbol='430090', begin='2019-07-03', end='2019-07-10')
        self.assertEqual(data.empty, False)

    def test_finance(self):
        data = self.client.finance(symbol='430090')
        self.assertEqual(data.empty, False)
