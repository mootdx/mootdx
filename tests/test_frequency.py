import unittest

from mootdx.quotes import Quotes


class TestFrequency(unittest.TestCase):
    def setUp(self) -> None:
        self.client = Quotes.factory(market='std')

    def test_to_data_empty(self):
        data = ['5m', '15m', '30m', '1h', 'day', 'week', 'mon', '1m', '1m', 'day', '3mon', 'year']

        for i, v in enumerate(data):
            assert all(self.client.bars(symbol='600036', frequency=i) == self.client.bars(symbol='600036', frequency=v))


if __name__ == '__main__':
    unittest.main()
