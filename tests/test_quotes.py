# -*- coding: utf-8 -*-
from mootdx.reader import Reader, ExReader
from mootdx.quotes import LiveBars, ExLiveBars
import unittest

class TestLiveBars(unittest.TestCase):
    reader = None

    ##初始化工作
    def setUp(self):
        self.client = LiveBars()
    
    #退出清理工作
    def tearDown(self):
        del self.client
    
    #具体的测试用例，一定要以test开头
    def testBars(self):
        data = self.client.bars(symbol='000001')
        self.assertNotNull(data)
        
        
    # def testMinbar(self):
    #     self.assertTrue(self.client.minute(symbol='000001'))
        
if __name__ =='__main__':
    unittest.main()
# def test_daily():
# 	assert reader.daily(symbol='000001') == True
