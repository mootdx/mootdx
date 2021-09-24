import unittest
from pathlib import Path

from mootdx import config
from mootdx.quotes import Quotes


class TestBestIP(unittest.TestCase):

    def setup_class(self):
        self.conf = Path.home() / '.mootdx' / 'config.json'

    def teardown_class(self):
        self.conf.unlink()

    def test_config(self):
        self.conf.unlink()

        config.setup()
        assert self.conf.exists()

    def test_quotes(self):
        self.conf.unlink()

        Quotes.factory(market='std', timeout=10)
        assert self.conf.exists()


if __name__ == '__main__':
    unittest.main()
