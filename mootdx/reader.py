# -*- coding: utf-8 -*-
import os

from pytdx.reader import (
    TdxExHqDailyBarReader,
    TdxLCMinBarReader,
    TdxDailyBarReader,
    BlockReader
)


# 股票市场
class Reader(object):
    """股票市场"""

    tdxdir = r'C:/new_tdx'

    def __init__(self, tdxdir=None):
        super(Reader, self).__init__()
        self.tdxdir = tdxdir

    # 寻找文件路径
    def find_path(self, stock=None, subdir='lday', ext='day'):
        '''
        寻找文件路径，辅助函数

        :param stock:
        :param subdir:
        :param ext:
        :return: pd.dataFrame or None
        '''
        paths = [
            'vipdoc/sz/%s/sz%s.%s' % (subdir, stock, ext),
            'vipdoc/sh/%s/sh%s.%s' % (subdir, stock, ext),
        ]

        for p in paths:
            path = os.path.join(self.tdxdir, p)
            if os.path.exists(path):
                return path

        return None

    # 日线
    def daily(self, symbol=None):
        '''
        获取日线数据

        :param symbol:
        :return: pd.dataFrame or None
        '''
        reader = TdxDailyBarReader()
        symbol = self.find_path(symbol)

        if not symbol is None:
            return reader.get_df(symbol)

        return None

    # 1分钟线
    def minute(self, symbol=None):
        '''
        获取1分钟线

        :param symbol:
        :return: pd.dataFrame or None
        '''
        symbol = self.find_path(symbol, subdir='minline', ext='lc1')
        symbol = self.find_path(symbol, subdir='minline', ext='1') if not symbol else symbol
        reader = TdxLCMinBarReader()

        if not symbol is None:
            return reader.get_df(symbol)

        return None

    # 5分钟线
    def fzline(self, symbol=None):
        '''
        获取5分钟线

        :param symbol:
        :return: pd.dataFrame or None
        '''
        symbol = self.find_path(symbol, subdir='fzline', ext='lc5')
        symbol = self.find_path(symbol, subdir='fzline', ext='5') if not symbol else symbol
        reader = TdxLCMinBarReader()

        if not symbol is None:
            return reader.get_df(symbol)

        return None

    # 板块
    def block(self, group=False, custom=False):
        '''

        :param group:
        :param custom:
        :return: pd.dataFrame or None
        '''
        reader = BlockReader()
        symbol = os.path.join(self.tdxdir, 'block_zs.dat')

        if not symbol is None:
            return reader.get_df(symbol, group)

        return None

        # 指数

    def index(self, symbol='incon.dat', group=False):
        '''

        :param symbol:
        :param group:
        :return: pd.dataFrame or None
        '''
        reader = BlockReader()
        symbol = os.path.join(self.tdxdir, symbol)

        if not symbol is None:
            return reader.get_df(symbol, group)

        return None


# 扩展市场读取
class ExReader(Reader):
    """扩展市场读取"""

    def daily(self, symbol=None):
        '''


        :return: pd.dataFrame or None
        '''
        reader = TdxExHqDailyBarReader()
        symbol = self.find_path(symbol)

        if symbol is not None:
            return reader.get_df(symbol)

        return None
