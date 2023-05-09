import unittest

import pytest

from mootdx.quotes import Quotes


@pytest.mark.skip(reason="暂时不做重复测试")
class TestStdQuotes(unittest.TestCase):
    client = None
    server = ("39.100.68.59", 7709)

    def test_server(self):
        client = Quotes.factory(market="std", server=self.server, verbose=2, timeout=10)  # 标准市场
        assert client.server == self.server

    def test_not_server(self):
        client = Quotes.factory(market="std", server=None, verbose=2, timeout=10)  # 标准市场
        assert client.server != self.server

    def test_empty_server(self):
        client = Quotes.factory(market="std", verbose=2, timeout=10)  # 标准市场
        assert client.server != self.server

    def test_set_server(self):
        client = Quotes.factory(market="std", server=self.server, verbose=2, timeout=10)  # 标准市场
        assert client.server == self.server, self.server

        server = ("112.74.214.43", 7727)
        client = Quotes.factory(market="ext", server=server, verbose=2, timeout=10)  # 标准市场
        assert client.server == server, server
