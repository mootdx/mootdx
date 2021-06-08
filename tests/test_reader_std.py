# -*- coding: utf-8 -*-

import unittest

from mootdx.reader import Reader


class TestReader(unittest.TestCase):
    reader = None

    # 初始化工作
    def setUp(self):
        self.reader = Reader.factory(market='std', tdxdir='../fixtures/vipdoc')

    # 退出清理工作
    def tearDown(self):
        self.reader = None

    def test_daily(self):
        self.assertFalse(self.reader.daily(symbol='688586').empty)

    # def test_block(self):
    #     self.assertFalse(self.reader.block(symbol='block_fg', group=True).empty)

    # def test_custom_block(self):
    # self.assertFalse(self.reader.block(symbol='blocknew', custom=True, group=True).empty)

    def test_minute1(self):
        result = self.reader.minute(symbol='688586', suffix='1')
        print(result)
        self.assertFalse(result.empty)

    def test_minute5(self):
        result = self.reader.minute(symbol='688586', suffix='5')
        print(result)
        self.assertFalse(result.empty)

    def test_block(self):
        result = self.reader.block(symbol='block_zs', group=True)
        print(result)
        self.assertFalse(result.empty)

    # def test_block_custom(self):
    #     result = self.reader.block(symbol='block_zs', custom=True)
    #     print(result)
    #     self.assertFalse(result.empty)


if __name__ == '__main__':
    unittest.main()
