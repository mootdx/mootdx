# -*- coding: utf-8 -*-
from pytdx.reader import (
    TdxFileNotFoundException,
    TdxExHqDailyBarReader, 
    CustomerBlockReader,
    TdxLCMinBarReader,
    TdxDailyBarReader, 
    TdxMinBarReader,
    BlockReader
)
import os

# 股票市场
class Reader(object):
    """股票市场"""

    tdxdir = r'C:/new_tdx'

    def __init__(self, tdxdir=None):
        super(Reader, self).__init__()
        self.tdxdir = tdxdir

    # 寻找文件路径
    def find_path(self, stock=None, subdir='lday', ext='day'):
        paths = [
            'vipdoc/sz/%s/sz%s.%s' % (subdir, stock, ext),
            'vipdoc/sh/%s/sh%s.%s' % (subdir, stock, ext),
        ]
        
        for p in paths:
            path = os.path.join(self.tdxdir, p)
            if os.path.exists(path):
                return path

        print('文件不存在')
        return None

    # 日线
    def daily(self, symbol=None):
        reader = TdxDailyBarReader()
        symbol = self.find_path(symbol)
        
        if not symbol is None:
            return reader.get_df(symbol)

        return None

    # 1分钟线
    def minbar(self, symbol=None):
        symbol = self.find_path(symbol, subdir='minline', ext='lc1')
        symbol = self.find_path(symbol, subdir='minline', ext='1') if not symbol else symbol
        reader = TdxLCMinBarReader()

        if not symbol is None:
            return reader.get_df(symbol)

        return None

    # 5分钟线
    def fzline(self, symbol=None):
        symbol = self.find_path(symbol, subdir='fzline', ext='lc5')
        symbol = self.find_path(symbol, subdir='fzline', ext='5') if not symbol else symbol     
        reader = TdxLCMinBarReader()

        if not symbol is None:
            return reader.get_df(symbol)

        return None

    # 板块
    def block(self, group=False, custom=False):
        reader = BlockReader()
        symbol = os.path.join(self.tdxdir, 'block_zs.dat')

        if not symbol is None:
            return reader.get_df(symbol, group)

        return None     
    
    # 指数
    def index(self, symbol='incon.dat', group=False):
        reader = BlockReader()
        symbol = os.path.join(self.tdxdir, symbol)
        
        if not symbol is None:
            return reader.get_df(symbol, group)

        return None

# 扩展市场读取
class ExReader(Reader):
    """扩展市场读取"""

    def ExDaily(symbol=None):
        reader = TdxExHqDailyBarReader()
        symbol = self.find_path(symbol)

        if not symbol is None:
            return reader.get_df(symbol)

        return None

        
