import unittest
from pathlib import Path

from mootdx import config
from mootdx.quotes import Quotes


class TestBestIP(unittest.TestCase):

    def test_config_setup(self):
        conf = Path.home() / '.mootdx' / 'config.json'
        conf.unlink()
        assert not conf.exists()

        config.setup()
        assert conf.exists()

    def test_quotes(self):
        conf = Path.home() / '.mootdx' / 'config.json'
        conf.unlink()
        assert not conf.exists()

        Quotes.factory(market='std', timeout=10)  # 标准市场
        assert conf.exists()


if __name__ == '__main__':
    unittest.main()
