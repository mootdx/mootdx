# -*- coding: utf-8 -*-
import os

from pytdx.reader import (BlockReader, TdxDailyBarReader,
                          TdxExHqDailyBarReader, TdxLCMinBarReader)

from mootdx.utils import get_stock_market


# 股票市场
class Reader(object):
    """股票市场"""

    tdxdir = r'C:/new_tdx'

    def __init__(self, tdxdir=None):
        super(Reader, self).__init__()
        self.tdxdir = tdxdir

    def find_path(self, symbol=None, subdir='lday', ext='day'):
        '''
        寻找文件路径，辅助函数

        :param symbol:
        :param subdir:
        :param ext:
        :return: pd.dataFrame or None
        '''
        market = get_stock_market(symbol, True)
        vipdoc = 'vipdoc/%s/%s/%s%s.%s' % (market, subdir, market, symbol, ext)
        vipdoc = os.path.join(self.tdxdir, vipdoc)

        if os.path.exists(vipdoc):
            return vipdoc

        return None

    def daily(self, symbol=None):
        '''
        获取日线数据

        :param symbol:
        :return: pd.dataFrame or None
        '''
        reader = TdxDailyBarReader()
        vipdoc = self.find_path(symbol=symbol, subdir='lday', ext='day')

        if not vipdoc is None:
            return reader.get_df(vipdoc)

        return None

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

    def block(self, group=False, custom=False):
        '''
        获取板块数据

        :param group:
        :param custom:
        :return: pd.dataFrame or None
        '''
        reader = BlockReader()
        symbol = os.path.join(self.tdxdir, 'block_zs.dat')

        if not symbol is None:
            return reader.get_df(symbol, group)

        return None

    def index(self, symbol='incon.dat', group=False):
        '''
        获取指数数据

        :param symbol:
        :param group:
        :return: pd.dataFrame or None
        '''
        reader = BlockReader()
        symbol = os.path.join(self.tdxdir, symbol)

        if not symbol is None:
            return reader.get_df(symbol, group)

        return None


class ExReader(Reader):
    """扩展市场读取"""

    def daily(self, symbol=None):
        '''
        获取日线数据

        :return: pd.dataFrame or None
        '''
        reader = TdxExHqDailyBarReader()
        symbol = self.find_path(symbol)

        if symbol is not None:
            return reader.get_df(symbol)

        return None
