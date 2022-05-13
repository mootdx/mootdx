import unittest

import pytest

from mootdx.consts import KLINE_DAILY
from mootdx.quotes import Quotes


@pytest.mark.skip(reason='暂时不做测试')
class TestExtQuotes(unittest.TestCase):
    client = None

    def setup_class(self):
        self.client = Quotes.factory(market='ext')

    def teardown_class(self):
        self.client = None

    def test_markets(self):
        data = self.client.markets()
        self.assertEqual(data.empty, False)

    def test_instrument(self):
        data = self.client.instrument(0, 100)
        self.assertEqual(data.empty, False)

    def test_instruments(self):
        data = self.client.instruments()
        self.assertEqual(data.empty, False)

    def test_quote(self):
        data = self.client.quote(market=42, symbol='IMCI')
        self.assertEqual(data.empty, False)

        data = self.client.quote(symbol='42#IMCI')
        self.assertEqual(data.empty, False)

    def test_minute(self):
        data = self.client.minute(market=42, symbol='IMCI')
        self.assertEqual(data.empty, False)
        data = self.client.minute(symbol='42#IMCI')
        self.assertEqual(data.empty, False)

    def test_minutes(self):
        data = self.client.minutes(market=47, symbol='IF1709')
        self.assertEqual(data.empty, False)

        data = self.client.minutes(market=47, symbol='IF9')
        self.assertIsNone(data)

    def test_bars(self):
        data = self.client.bars(market=31, frequency=KLINE_DAILY, symbol='00020')
        self.assertEqual(data.empty, False)

    def test_transaction(self):
        data = self.client.transaction(market=47, symbol='IFL0')
        self.assertEqual(data.empty, False)

        data = self.client.transaction(market=31, symbol='00020')
        self.assertIsNone(data)

    def test_transactions(self):
        data = self.client.transactions(market=47, symbol='IFL0', date='20170810', start=1800)
        self.assertEqual(data.empty, False)


if __name__ == '__main__':
    unittest.main()
