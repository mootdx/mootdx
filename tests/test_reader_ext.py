# -*- coding: utf-8 -*-

import unittest

from mootdx.reader import Reader


class TestExReader(unittest.TestCase):
    reader = None

    # 初始化工作
    def setUp(self):
        self.reader = Reader.factory(market='ext', tdxdir='../fixtures')

    # 退出清理工作
    def tearDown(self):
        pass

    # 具体的测试用例，一定要以test开头
    def testDaily(self):
        data = self.reader.daily(symbol='27#CES100')
        print(data)
        self.assertTrue(data is not None)

    # def testMinbar(self):
    #     self.assertTrue(not self.reader.minute(symbol='27#CES100') is None)


if __name__ == '__main__':
    unittest.main()
