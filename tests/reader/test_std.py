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
        self.reader = None

    def test_daily(self):
        self.assertTrue(self.reader.daily(symbol='600036') is not None)

    def test_block(self):
        self.assertTrue(self.reader.block(type='zs') is not None)

    def test_minute1(self):
        self.assertTrue(self.reader.minute(symbol='600036', suffix='1') is not None)

    def test_minute5(self):
        self.assertTrue(self.reader.minute(symbol='600036', suffix='5') is not None)




if __name__ == '__main__':
    unittest.main()
