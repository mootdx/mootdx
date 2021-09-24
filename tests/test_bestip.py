import logging
import unittest
from pathlib import Path

import pytest

from mootdx import config
from mootdx.quotes import Quotes


class TestBestIP:

    def setup_class(self):
        self.conf = Path.home() / '.mootdx' / 'config.json'

    def teardown_class(self):
        pass

    @pytest.mark.skip('skip')
    def test_config(self, caplog):
        caplog.set_level(logging.WARNING)
        self.conf.exists() and self.conf.unlink()

        config.setup()
        # assert '未找到配置文件' in caplog.records
        assert self.conf.exists()

    def test_quotes(self):
        self.conf.exists() and self.conf.unlink()

        Quotes.factory(market='std', timeout=10)
        assert self.conf.exists()


if __name__ == '__main__':
    unittest.main()
