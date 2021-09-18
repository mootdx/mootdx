import unittest

from mootdx.consts import MARKET_SH
from mootdx.logger import log
from mootdx.quotes import Quotes


class TestStdQuotes(unittest.TestCase):
    client = None

    # 初始化工作
    def setup_class(self):
        self.client = Quotes.factory(market='std', timeout=10)  # 标准市场
        log.success('初始化工作')

    # 退出清理工作
    def teardown_class(self):
        self.client.client.close()
        del self.client
        log.success('退出清理工作')

    def test_quotes(self):
        data = self.client.quotes(symbol='600036')
        self.assertEqual(data.empty, False)

        data = self.client.quotes(symbol='688597')
        self.assertEqual(data.empty, False)

        data = self.client.quotes(symbol=['600036', '600016'])
        self.assertEqual(data.empty, False)

    def test_bars(self):
        data = self.client.bars(symbol='600036', frequency=9, offset=10)
        self.assertEqual(data.empty, False)

    def test_index(self):
        data = self.client.index(frequency=9, market=MARKET_SH, symbol='000001', start=1, offset=2)
        self.assertEqual(data.empty, False)

    def test_minute(self):
        data = self.client.minute(symbol='000001')
        self.assertEqual(data.empty, False)

    def test_minutes(self):
        data = self.client.minutes(symbol='000001', date='20171010')
        self.assertEqual(data.empty, False)

    def test_transaction(self):
        data = self.client.transaction(symbol='600036', start=0, offset=10)
        self.assertEqual(data.empty, False)

    def test_transactions(self):
        data = self.client.transactions(symbol='600036', start=0, offset=10, date='20170209')
        self.assertEqual(data.empty, False)

    def test_F10C(self):
        data = self.client.F10C(symbol='000001')
        self.assertTrue(data)

    def test_F10(self):
        data = self.client.F10(symbol='000001', name='龙虎榜单')
        self.assertTrue(data)

    def test_xdxr(self):
        data = self.client.xdxr(symbol='600036')
        self.assertEqual(data.all().empty, False)

    def test_k(self):
        data = self.client.k(symbol='000001', begin='2019-07-03', end='2019-07-10')
        self.assertEqual(data.empty, False)

    def test_block(self):
        data = self.client.block()
        self.assertEqual(data.empty, False)

    def test_finance(self):
        data = self.client.finance(symbol='000001')
        self.assertEqual(data.empty, False)
