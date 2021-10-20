import logging
from pathlib import Path

import pytest

from mootdx import config


class TestBestIP:
    config = ''

    @staticmethod
    def setup_class(cls):
        logging.info('setup_class')
        cls.config = Path.home() / '.mootdx' / 'config.json'
        cls.config.exists() and cls.config.unlink()

    @staticmethod
    def teardown_class(cls):
        logging.info('teardown_class')
        cls.config.exists() and cls.config.unlink()

    @pytest.mark.skip('skip')
    def test_config(self, caplog):
        caplog.set_level(logging.WARNING)
        self.config.exists() and self.config.unlink()

        config.setup()
        assert self.config.exists(), self.config

    def test_quotes(self):
        config.setup()
        assert self.config.exists(), self.config
