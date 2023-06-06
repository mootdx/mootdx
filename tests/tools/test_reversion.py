import unittest

from mootdx.quotes import Quotes
from mootdx.tools.reversion import reversion
from mootdx.utils.adjust import get_xdxr


class TestReversion(unittest.TestCase):
    client = None
    symbol = '600000'

    # 初始化工作
    def setup_class(self):
        self.client = Quotes.factory(market='std', timeout=10)  # 标准市场

    # 退出清理工作
    def teardown_class(self):
        self.client.client.close()
        del self.client

    def test_get_xdxr(self):
        # data = self.client.bars(symbol=self.symbol)
        xdxr = get_xdxr(symbol=self.symbol)

        assert xdxr.empty is False
        assert 'code' in xdxr.columns

    def test_reversion(self):
        data = self.client.bars(symbol=self.symbol)
        xdxr = get_xdxr(symbol=self.symbol)

        reversion(data, xdxr, 'qfq')
        # self.assertFalse(result.empty)

    def test_to_qfq(self):
        data = self.client.bars(symbol=self.symbol, offset=800)
        xdxr = get_xdxr(symbol=self.symbol)

        data0 = reversion(data, xdxr, 'qfq')
        assert data0.empty is False

        data1 = self.client.bars(symbol=self.symbol, offset=800, adjust='Qfq')
        assert data1.empty is False
        assert data1.equals(data0)

    def test_to_hfq(self):
        data = self.client.bars(symbol=self.symbol, offset=800)
        xdxr = get_xdxr(symbol=self.symbol)

        data0 = reversion(data, xdxr, 'hfq')
        assert data.empty is False

        data1 = self.client.bars(symbol=self.symbol, offset=800, adjust='HFQ')
        assert data1.empty is False
        assert data1.equals(data0)
