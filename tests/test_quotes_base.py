import pytest
import unittest

from mootdx.logger import logger
from mootdx.quotes import Quotes


class TestStdQuotes(unittest.TestCase):
    client = None
    bestip = ("39.100.68.59", 7709)

    def test_bestip(self):
        client = Quotes.factory(market="std", server=self.bestip, verbose=2, timeout=10)  # 标准市场
        assert client.bestip == self.bestip

    def test_not_bestip(self):
        client = Quotes.factory(market="std", server=None, verbose=2, timeout=10)  # 标准市场
        assert client.bestip != self.bestip

    def test_empty_bestip(self):
        client = Quotes.factory(market="std", verbose=2, timeout=10)  # 标准市场
        assert client.bestip != self.bestip
