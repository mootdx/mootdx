# -*- coding: utf-8 -*-
import os

from mootdx.utils import get_stock_market
from pytdx.reader import (BlockReader, TdxDailyBarReader,
                          TdxExHqDailyBarReader, TdxLCMinBarReader)


# 股票市场
class Reader(object):
    @staticmethod
    def factory(market='std', **kwargs):
        if market == 'ext':
            return ExtReader(**kwargs)
        elif market == 'std':
            return StdReader(**kwargs)


class ReaderBase(object):
    """股票市场"""

    tdxdir = 'C:/new_tdx'

    def __init__(self, tdxdir=None):
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
        ext = ext if isinstance(ext, list) else [ext]

        for t in ext:
            vipdoc = 'vipdoc/{}/{}/{}{}.{}'.format(market, subdir, market, symbol, t)
            vipdoc = os.path.join(self.tdxdir, vipdoc)

            if os.path.exists(vipdoc):
                return vipdoc

        return None

class StdReader(ReaderBase):
    """股票市场"""

    def daily(self, symbol=None):
        '''
        获取日线数据

        :param symbol:
        :return: pd.dataFrame or None
        '''
        reader = TdxDailyBarReader()
        vipdoc = self.find_path(symbol=symbol, subdir='lday', ext='day')

        if vipdoc is not None:
            return reader.get_df(vipdoc)

        return None

    def minute(self, symbol=None, suffix='1'):
        '''
        获取1,5分钟线

        :param symbol:
        :return: pd.dataFrame or None
        '''
        subdir = 'fzline' if str(suffix) == '5' else 'minline'
        suffix = ['lc5', '5'] if str(suffix) == '5' else ['lc1', '1']
        symbol = self.find_path(symbol, subdir=subdir, ext=suffix)
        reader = TdxLCMinBarReader()

        if symbol is not None:
            return reader.get_df(symbol)

        return None


    def fzline(self, symbol=None):
        return self.minute(symbol, suffix='5')


    def block(self, category='', market='sh', group=False, custom=False):
        '''
        获取板块数据

        :param group:
        :param custom:
        :return: pd.dataFrame or None
        '''
        reader = BlockReader()
        symbol = os.path.join(self.tdxdir, 'block_{}.dat'.format(category))

        if symbol is not None:
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

        if symbol is not None:
            return reader.get_df(symbol, group)

        return None


class ExtReader(ReaderBase):
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
