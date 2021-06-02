# -*- coding: utf-8 -*-
import os

from pytdx.reader import (BlockReader, CustomerBlockReader, TdxDailyBarReader,
                          TdxExHqDailyBarReader, TdxLCMinBarReader)

from mootdx.consts import TYPE_GROUP
from mootdx.logger import log
from mootdx.utils import get_stock_market


class MooTdxDailyBarReader(TdxDailyBarReader):
    SECURITY_TYPE = ["SH_A_STOCK", "SH_B_STOCK", "SH_STAR_STOCK", "SH_INDEX", "SH_FUND", "SH_BOND", "SZ_A_STOCK", "SZ_B_STOCK", "SZ_INDEX", "SZ_FUND", "SZ_BOND"]
    SECURITY_COEFFICIENT = {"SH_A_STOCK": [0.01, 0.01], "SH_B_STOCK": [0.001, 0.01], "SH_STAR_STOCK": [0.01, 0.01], "SH_INDEX": [0.01, 1.0], "SH_FUND": [0.001, 1.0],
                            "SH_BOND": [0.001, 1.0], "SZ_A_STOCK": [0.01, 0.01], "SZ_B_STOCK": [0.01, 0.01], "SZ_INDEX": [0.01, 1.0], "SZ_FUND": [0.001, 0.01],
                            "SZ_BOND": [0.001, 0.01]}

    def get_security_type(self, fname):

        exchange = str(fname[-12:-10]).lower()
        code_head = fname[-10:-8]

        if exchange == self.SECURITY_EXCHANGE[0]:
            if code_head in ["00", "30"]:
                return "SZ_A_STOCK"
            elif code_head in ["20"]:
                return "SZ_B_STOCK"
            elif code_head in ["39"]:
                return "SZ_INDEX"
            elif code_head in ["15", "16"]:
                return "SZ_FUND"
            elif code_head in ["10", "11", "12", "13", "14"]:
                return "SZ_BOND"
        elif exchange == self.SECURITY_EXCHANGE[1]:
            if code_head in ["60"]:
                return "SH_A_STOCK"
            elif code_head in ["90"]:
                return "SH_B_STOCK"
            elif code_head in ["68"]:
                return "SH_STAR_STOCK"
            elif code_head in ["00", "88", "99"]:
                return "SH_INDEX"
            elif code_head in ["50", "51"]:
                return "SH_FUND"
            elif code_head in ["01", "10", "11", "12", "13", "14"]:
                return "SH_BOND"
        else:
            print("Unknown security exchange !\n")
            raise NotImplementedError


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


class ReaderBase(object):
    """股票市场"""

    # 默认通达信安装目录
    tdxdir = 'C:/new_tdx'

    def __init__(self, tdxdir=None):
        """
        构造函数

        :param tdxdir: 通达信安装目录
        """

        if os.path.isdir(tdxdir):
            self.tdxdir = tdxdir
        else:
            log.error('tdxdir 目录不存在')

    def find_path(self, symbol=None, subdir='lday', ext=None):
        """
        自动匹配文件路径，辅助函数

        :param symbol:
        :param subdir:
        :param ext:
        :return: pd.dataFrame or None
        """
        market = get_stock_market(symbol, True) if len(symbol.split('#')) == 1 else 'ds'
        prefix = market if len(symbol.split('#')) == 1 else ''
        ext = ext if isinstance(ext, list) else [ext]

        for t in ext:
            vipdoc = 'vipdoc/{}/{}/{}{}.{}'.format(market, subdir, prefix, symbol, t)
            vipdoc = os.path.join(self.tdxdir, vipdoc)

            if os.path.exists(vipdoc):
                return vipdoc
            else:
                log.error('未找到所需的文件: {}'.format(vipdoc))

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
        vipdoc = self.find_path(symbol=symbol, subdir='lday', ext='day')

        if vipdoc is not None:
            return reader.get_df(vipdoc)

        return None

    def minute(self, symbol=None, suffix=1):
        """
        获取1,5分钟线

        :param suffix:
        :param symbol:
        :return: pd.dataFrame or None
        """
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
        """
        获取板块数据
        参考: http://blog.sina.com.cn/s/blog_623d2d280102vt8y.html

        :param custom:
        :param symbol:
        :param group:
        :return: pd.dataFrame or None
        """
        if custom:
            reader = CustomerBlockReader()
            vipdoc = os.path.join(self.tdxdir, 'T0002', 'blocknew', '{}'.format(symbol))
        else:
            reader = BlockReader()
            vipdoc = os.path.join(self.tdxdir, 'T0002', 'hq_cache', '{}.dat'.format(symbol))

        fmt = TYPE_GROUP if group else None

        if os.path.exists(vipdoc):
            return reader.get_df(vipdoc, fmt)
        else:
            log.error('未找到所需的文件: {}'.format(vipdoc))

        return None


class ExtReader(ReaderBase):
    """扩展市场读取"""

    def daily(self, symbol=None):
        """
        获取日线数据

        :return: pd.dataFrame or None
        """
        reader = TdxExHqDailyBarReader()
        vipdoc = self.find_path(symbol=symbol, subdir='lday', ext='day')

        if symbol is not None:
            return reader.get_df(vipdoc)

        return None
