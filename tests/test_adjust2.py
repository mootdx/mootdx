import unittest

import pytest
from loguru import logger

from mootdx.quotes import Quotes
from mootdx.utils import to_adjust


class TestAdjust2(unittest.TestCase):
    client = None

    # 初始化工作
    def setup_class(self):
        self.client = Quotes.factory(market='std', timeout=10)  # 标准市场

    # 退出清理工作
    def teardown_class(self):
        self.client.client.close()
        del self.client

    @pytest.mark.skip(reason='暂时不做测试')
    def test_to_data(self):
        result = self.client.bars(symbol='600036', adjust='qfq')
        self.assertFalse(result.empty)

    def test_to_adjust(self):
        result = self.client.bars(symbol='600036')
        result = to_adjust(result, symbol='sh600036', adjust='qfq')

        logger.info(result)
        assert not result.empty, result


if __name__ == '__main__':
    unittest.main()
