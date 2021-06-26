# -*- coding: utf-8 -*-

import unittest

from mootdx.reader import Reader


class TestExReader(unittest.TestCase):
    reader = None

    # 初始化工作
    def setUp(self):
        self.reader = Reader.factory(market='ext', tdxdir='tests/fixtures')

    # 退出清理工作
    def tearDown(self):
        pass

    # 具体的测试用例，一定要以test开头
    def test_daily(self):
        data = self.reader.daily(symbol='4#CF7D0LAO')
        self.assertFalse(data.empty)

    def test_minbar(self):
        data = self.reader.minute(symbol='4#CF7D0LAO')
        print(data)
        self.assertFalse(data.empty)

if __name__ == '__main__':
    unittest.main()
