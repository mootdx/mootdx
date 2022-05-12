import pytest

from mootdx.quotes import Quotes
from mootdx.utils.adjust import to_adjust
from mootdx.logger import logger


class TestFactor:

    # 初始化工作
    def setup_class(self):
        self.client = Quotes.factory(market='std', timeout=10)  # 标准市场
        logger.success('初始化工作')

    def test_qfq_factor(self):
        result = self.client.bars(symbol='600036', adjust='qfq')
        assert len(result), result

    def test_hfq_factor(self):
        result = self.client.bars(symbol='600036', adjust='hfq')
        assert len(result), result
