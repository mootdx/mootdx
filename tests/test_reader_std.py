# # -*- coding: utf-8 -*-
#
# import unittest
#
# from mootdx.reader import Reader, ReaderBase
#
#
# class TestReader(unittest.TestCase):
#     reader = None
#
#     # 初始化工作
#     def setUp(self):
#         self.reader = Reader.factory(market='std', tdxdir='tests/fixtures')
#
#     # 退出清理工作
#     def tearDown(self):
#         self.reader = None
#
#     def test_daily(self):
#         self.assertFalse(self.reader.daily(symbol='000001').empty)
#
#     def test_block(self):
#         # self.assertFalse(self.reader.block(symbol='block', group=True).empty)
#         self.assertFalse(self.reader.block(symbol='block_fg', group=True).empty)
#         self.assertFalse(self.reader.block(symbol='block_gn', group=True).empty)
#         self.assertFalse(self.reader.block(symbol='block_zs', group=True).empty)
#         # self.assertFalse(self.reader.block(symbol='tdxhy.cfg', group=True).empty)
#
#     def test_custom_block(self):
#         self.assertFalse(self.reader.block_new(group=True).empty)
#
#     def test_minute1(self):
#         result = self.reader.minute(symbol='688001', suffix='1')
#         print(result)
#         self.assertFalse(result.empty)
#
#     def test_minute5(self):
#         result = self.reader.minute(symbol='688001', suffix='5')
#         print(result)
#         self.assertFalse(result.empty)
#
#     def test_blocks(self):
#         result = self.reader.block(symbol='block_zs', group=True)
#         print(result)
#         self.assertFalse(result.empty)
#
#     # def test_block_custom(self):
#     #     result = self.reader.block(symbol='block_zs', custom=True)
#     #     print(result)
#     #     self.assertFalse(result.empty)
#
#
# class TestReaderBase(unittest.TestCase):
#     def test_find_path(self):
#         reader = ReaderBase('tests/fixtures')
#         result = reader.find_path(symbol='688001', subdir='minline', suffix=['lc1', '1'])
#         self.assertIsNotNone(result)
#
#
# if __name__ == '__main__':
#     unittest.main()
