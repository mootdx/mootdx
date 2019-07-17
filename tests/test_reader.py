# -*- coding: utf-8 -*-

import unittest

from mootdx.reader import Reader


class TestReader(unittest.TestCase):
    reader = None

    # 初始化工作
    def setUp(self):
        self.reader = Reader.factory(market='std', tdxdir='./tests/data')

    # 退出清理工作
    def tearDown(self):
        pass

    # 具体的测试用例，一定要以test开头
    def testDaily(self):
        self.assertTrue(self.reader.daily(symbol='600036') is not None)

    def testMinbar(self):
        self.assertTrue(self.reader.minute(symbol='600036') is not None)

    def fzlineMinbar(self):
        self.assertTrue(self.reader.fzline(symbol='600036') is not None)


class TestExReader(unittest.TestCase):
    reader = None

    # 初始化工作
    def setUp(self):
        self.reader = Reader.factory(market='ext', tdxdir='./tests/data')

    # 退出清理工作
    def tearDown(self):
        pass

    # 具体的测试用例，一定要以test开头
    def testDaily(self):
        self.assertTrue(not self.reader.daily(symbol='600036') is None)

    def testMinbar(self):
        self.assertTrue(not self.reader.minute(symbol='600036') is None)


if __name__ == '__main__':
    unittest.main()
