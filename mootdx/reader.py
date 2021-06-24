# -*- coding: utf-8 -*-
from abc import ABC

from pytdx.reader import (BlockReader, CustomerBlockReader, TdxExHqDailyBarReader, TdxLCMinBarReader)
from unipath import Path

from mootdx import utils
from mootdx.consts import TYPE_GROUP
from mootdx.contrib.compat import MooTdxDailyBarReader
from mootdx.logger import log
from mootdx.utils import get_stock_market


# 股票市场
class Reader(object):
    @staticmethod
    def factory(market='std', **kwargs):
        """
        Reader 工厂方法

        :param market:  std 标准市场, ext 扩展市场
        :param kwargs:
        :return:
        """
        if market == 'ext':
            return ExtReader(**kwargs)
        elif market == 'std':
            return StdReader(**kwargs)


class ReaderBase(ABC):
    """股票市场"""

    # 默认通达信安装目录
    tdxdir = 'C:/new_tdx'

    def __init__(self, tdxdir=None):
        """
        构造函数

        :param tdxdir: 通达信安装目录
        """

        if Path(tdxdir).isdir():
            self.tdxdir = tdxdir
        else:
            log.error('tdxdir 目录不存在')
            raise Exception('tdxdir 目录不存在')

    def find_path(self, symbol=None, subdir='lday', suffix=None):
        """
        自动匹配文件路径，辅助函数

        :param symbol:
        :param subdir:
        :param suffix:
        :return: pd.dataFrame or None
        """
        market = get_stock_market(symbol, True) if len(symbol.split('#')) == 1 else 'ds'
        prefix = market if len(symbol.split('#')) == 1 else ''
        suffix = suffix if isinstance(suffix, list) else [suffix]

        for ex_ in suffix:
            ex_ = ex_.strip('.')
            vipdoc = Path(self.tdxdir, 'vipdoc', market, subdir, f'{prefix}{symbol}.{ex_}')

            if not Path(vipdoc).exists():
                log.debug(f'未找到所需的文件: {vipdoc}')
                continue

            log.debug(f"找到所需的文件: {vipdoc}")
            return vipdoc

        return None


class StdReader(ReaderBase):
    """股票市场"""

    def daily(self, symbol=None):
        """
        获取日线数据

        :param symbol:
        :return: pd.dataFrame or None
        """
        reader = MooTdxDailyBarReader()
        vipdoc = self.find_path(symbol=symbol, subdir='lday', suffix='day')

        if vipdoc is not None:
            return reader.get_df(vipdoc)

        return None

    def minute(self, symbol=None, suffix=1):
        """
        获取1, 5分钟线

        :param suffix:
        :param symbol:
        :return: pd.dataFrame or None
        """
        subdir = 'fzline' if str(suffix) == '5' else 'minline'
        suffix = ['lc5', '5'] if str(suffix) == '5' else ['lc1', '1']
        symbol = self.find_path(symbol, subdir=subdir, suffix=suffix)
        reader = TdxLCMinBarReader()

        if symbol is not None:
            return reader.get_df(symbol)

        return None

    def fzline(self, symbol=None):
        """
        分钟线数据

        :param symbol: 自定义板块股票列表, 类型 list
        :return: pd.dataFrame or Bool
        """
        return self.minute(symbol, suffix=5)

    def block_new(self, name: str = None, symbol: list = None, group=False):
        """
        自定义板块数据操作
        提示: name 和 symbol 全为空则为读取，否则写入操作
        参考: http://blog.sina.com.cn/s/blog_623d2d280102vt8y.html

        :param name: 自定义板块名称
        :param symbol: 自定义板块股票列表, 类型 list
        :param group:
        :return: pd.dataFrame or Bool
        """

        if name or symbol:
            return utils.block_new(self.tdxdir, name=name, symbol=symbol)

        reader = CustomerBlockReader()
        vipdoc = Path(self.tdxdir, 'T0002', 'blocknew')

        fmt = TYPE_GROUP if group else None

        if Path(vipdoc).isdir():
            log.debug(f'找到所需的文件: {vipdoc}')
            return reader.get_df(vipdoc, fmt)

        log.error(f'未找到所需的文件: {vipdoc}')

        return None

    def block(self, symbol='', custom=False, group=False):
        """
        获取板块数据
        参考: http://blog.sina.com.cn/s/blog_623d2d280102vt8y.html

        :param custom:
        :param symbol:
        :param group:
        :return: pd.dataFrame or None
        """

        # suffix = symbol.split('.')
        # suffix = suffix[-1] if len(suffix) > 1 else 'dat'
        suffix = 'dat'
        # symbol = suffix[0]

        reader = BlockReader()
        vipdoc = Path(self.tdxdir, 'T0002', 'hq_cache', f'{symbol}.{suffix}')

        fmt = TYPE_GROUP if group else None

        if Path(vipdoc).exists():
            return reader.get_df(vipdoc, fmt)

        log.error(f'未找到所需的文件: {vipdoc}')

        return None


class ExtReader(ReaderBase):
    """扩展市场读取"""

    def __init__(self, tdxdir=None):
        super(ExtReader, self).__init__(tdxdir)
        self.reader = TdxExHqDailyBarReader()

    def daily(self, symbol=None, *args, **kwargs):
        """
        获取扩展市场日线数据

        :return: pd.dataFrame or None
        """
        vipdoc = self.find_path(symbol=symbol, subdir='lday', suffix='day')

        if symbol is not None:
            return self.reader.get_df(vipdoc)

        return None

    def minute(self, symbol=None, *args, **kwargs):
        """
        获取扩展市场分钟线数据

        :return: pd.dataFrame or None
        """
        vipdoc = self.find_path(symbol=symbol, subdir='minline', suffix=['lc1','1'])

        if symbol is not None:
            return self.reader.get_df(vipdoc)

        return None

    def fzline(self, symbol=None, *args, **kwargs):
        """
        获取日线数据

        :return: pd.dataFrame or None
        """
        vipdoc = self.find_path(symbol=symbol, subdir='fzline', suffix='lc5')

        if symbol is not None:
            return self.reader.get_df(vipdoc)

        return None
