# -*- coding: utf-8 -*-
from mootdx.reader import Reader, ExReader
from mootdx.quotes import LiveBar, ExLiveBar
import unittest

class TestLiveBar(unittest.TestCase):
    reader = None

    ##初始化工作
    def setUp(self):
        self.client = LiveBar()
    
    #退出清理工作
    def tearDown(self):
        del self.client
    
    #具体的测试用例，一定要以test开头
    def testBars(self):
        data = self.client.bars(symbol='000001')
        self.assertTrue(data is not None)
        
        
    # def testMinbar(self):
    #     self.assertTrue(self.client.minute(symbol='000001'))
        
if __name__ =='__main__':
    unittest.main()
# def test_daily():
# 	assert reader.daily(symbol='000001') == True
