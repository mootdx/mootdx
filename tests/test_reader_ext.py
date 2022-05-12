import unittest

from mootdx.reader import Reader
from tests.conftest import is_empty


class TestExReader(unittest.TestCase):
    reader = None

    # 初始化工作
    def setUp(self):
        self.reader = Reader.factory(market='ext', tdxdir='../fixtures')

    # 退出清理工作
    def tearDown(self):
        pass

    # 具体的测试用例，一定要以test开头
    def test_daily(self):
        data = self.reader.daily(symbol='4#CF7D0LAO')
        assert is_empty(data) is False

        data = self.reader.daily(symbol='4#xxx')
        assert is_empty(data) is True

    def test_minute(self):
        data = self.reader.minute(symbol='4#CF7D0LAO')
        assert is_empty(data) is True


if __name__ == '__main__':
    unittest.main()
