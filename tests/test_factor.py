from pprint import pprint

from mootdx.logger import logger
from mootdx.quotes import Quotes
from mootdx.reader import Reader


class TestFactor:

    # 初始化工作
    def setup_class(self):
        self.client = Quotes.factory(market="std", timeout=10)  # 标准市场
        self.reader = Reader.factory(market="std", tdxdir="../fixtures")
        logger.success("初始化工作")

    def test_qfq_factor(self):
        result = self.client.bars(symbol="600036", adjust="qfq")
        assert len(result), result

    def test_hfq_factor(self):
        result = self.client.bars(symbol="600036", adjust="hfq")
        assert len(result), result

    def test_reader_qfq(self):
        result = self.reader.daily(symbol="688001", adjust="qfq")
        assert not result.empty, "股票代码不存在"
        print('')
        pprint(result.tail())

    def test_reader_hfq(self):
        result = self.reader.daily(symbol="688001", adjust="hfq")
        assert not result.empty, "股票代码不存在"
        print('')
        pprint(result.tail())
