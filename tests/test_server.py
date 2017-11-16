# -*- coding: utf-8 -*-

from mootdx.reader import Reader, ExReader
from mootdx.market import LiveBars, ExLiveBars
import unittest

class TestLiveBars(unittest.TestCase):
    reader = None

    ##初始化工作
    def setUp(self):
        self.reader = Reader(tdxdir='/Volumes/BOOTCAMP/new_tdx')
    
    #退出清理工作
    def tearDown(self):
        pass
    
    #具体的测试用例，一定要以test开头
    def testDaily(self):
        self.assertTrue(self.reader.daily(stock='000001'))
        
        
    def testMinbar(self):
        self.assertTrue(self.reader.minbar(stock='000001'))
        
class TestExLiveBars(unittest.TestCase):
    reader = None

    ##初始化工作
    def setUp(self):
        self.reader = Reader(tdxdir='/Volumes/BOOTCAMP/new_tdx')
    
    #退出清理工作
    def tearDown(self):
        pass
    
    #具体的测试用例，一定要以test开头
    def testDaily(self):
        self.assertTrue(self.reader.daily(stock='000001'))
        
        
    def testMinbar(self):
        self.assertTrue(self.reader.minbar(stock='000001'))
        
if __name__ =='__main__':
    unittest.main()
# def test_daily():
# 	assert reader.daily(stock='000001') == True