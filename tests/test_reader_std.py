# -*- coding: utf-8 -*-

import unittest

from mootdx.reader import Reader


class TestReader(unittest.TestCase):
    reader = None

    # 初始化工作
    def setUp(self):
        self.reader = Reader.factory(market='std', tdxdir='../fixtures')

    # 退出清理工作
    def tearDown(self):
        self.reader = None

    def test_daily(self):
        self.assertTrue(self.reader.daily(symbol='600000') is not None)

    # def test_block(self):
    #     self.assertTrue(self.reader.block(symbol='block_fg', group=True) is not None)

    # def test_custom_block(self):
    # self.assertTrue(self.reader.block(symbol='blocknew', custom=True, group=True) is not None)

    def test_minute1(self):
        self.assertTrue(
            self.reader.minute(symbol='600000', suffix='1') is not None)

    def test_minute5(self):
        self.assertTrue(
            self.reader.minute(symbol='600000', suffix='5') is not None)

    def test_block(self):
        result = self.reader.block(symbol='block_zs', group=True)
        print(result)
        self.assertTrue(result is not None)

    def test_block_custom(self):
        result = self.reader.block(symbol='block_zs', custom=True)
        print(result)
        self.assertTrue(result is not None)


if __name__ == '__main__':
    unittest.main()
