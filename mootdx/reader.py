# -*- coding: utf-8 -*-
import logging
import os

from pytdx.reader import (BlockReader, TdxDailyBarReader, CustomerBlockReader,
                          TdxExHqDailyBarReader, TdxLCMinBarReader)

from mootdx.consts import TYPE_GROUP
from mootdx.utils import get_stock_market

logger = logging.getLogger(__name__)


# 股票市场
class Reader(object):
    @staticmethod
    def factory(market='std', **kwargs):
        '''

        :param market:
        :param kwargs:
        :return:
        '''
        if market == 'ext':
            return ExtReader(**kwargs)
        elif market == 'std':
            return StdReader(**kwargs)


class ReaderBase(object):
    """股票市场"""

    # 默认通达信安装目录
    tdxdir = 'C:/new_tdx'

    def __init__(self, tdxdir=None):
        '''
        构造函数

        :param tdxdir: 通达信安装目录
        '''

        if os.path.isdir(tdxdir):
            self.tdxdir = tdxdir
        else:
            logger.error('tdxdir 目录不存在')

    def find_path(self, symbol=None, subdir='lday', ext=None):
        '''
        自动匹配文件路径，辅助函数

        :param symbol:
        :param subdir:
        :param ext:
        :return: pd.dataFrame or None
        '''
        market = get_stock_market(symbol, True) if len(symbol.split('#')) == 1 else 'ds'
        prefix = market if len(symbol.split('#')) == 1 else ''
        ext = ext if isinstance(ext, list) else [ext]

        for t in ext:
            vipdoc = 'vipdoc/{}/{}/{}{}.{}'.format(market, subdir, prefix, symbol, t)
            vipdoc = os.path.join(self.tdxdir, vipdoc)

            if os.path.exists(vipdoc):
                return vipdoc
            else:
                logger.error('未找到所需的文件: {}'.format(vipdoc))

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

    def minute(self, symbol=None, suffix=1):
        '''
        获取1,5分钟线

        :param suffix:
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
        return self.minute(symbol, suffix=5)

    def block(self, symbol='block', custom=False, group=False):
        '''
        获取板块数据
        参考: http://blog.sina.com.cn/s/blog_623d2d280102vt8y.html

        :param custom:
        :param symbol:
        :param group:
        :return: pd.dataFrame or None
        '''
        if custom:
            reader = CustomerBlockReader()
            vipdoc = os.path.join(self.tdxdir, 'T0002', 'blocknew', '{}'.format(symbol))
        else:
            reader = BlockReader()
            vipdoc = os.path.join(self.tdxdir, 'T0002', 'hq_cache', '{}.dat'.format(symbol))

        format = TYPE_GROUP if group else None

        if os.path.exists(vipdoc):
            return reader.get_df(vipdoc, format)
        else:
            logger.error('未找到所需的文件: {}'.format(vipdoc))

        return None


class ExtReader(ReaderBase):
    """扩展市场读取"""

    def daily(self, symbol=None):
        '''
        获取日线数据

        :return: pd.dataFrame or None
        '''
        reader = TdxExHqDailyBarReader()
        vipdoc = self.find_path(symbol=symbol, subdir='lday', ext='day')

        if symbol is not None:
            return reader.get_df(vipdoc)

        return None
