import logging
import unittest

from mootdx.logger import logger
from mootdx.quotes import Quotes


@unittest.skip(reason='暂时不做重复测试')
class TestBestIP(unittest.TestCase):
    def setup(self):
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        logger.addHandler(ch)
        logger.setLevel(logging.DEBUG)

    def test_normal(self):
        Quotes.factory(market='std', bestip=True)
