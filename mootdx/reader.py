from abc import ABC
from pathlib import Path

from pytdx.reader import BlockReader
from pytdx.reader import CustomerBlockReader
from pytdx.reader import TdxExHqDailyBarReader
from pytdx.reader import TdxLCMinBarReader
from pytdx.reader import TdxMinBarReader

from mootdx import utils
from mootdx.consts import TYPE_GROUP, TYPE_FLATS
from mootdx.contrib.compat import MooTdxDailyBarReader
from mootdx.utils import get_stock_market


# 股票市场
class Reader(object):
    @staticmethod
    def factory(market='std', **kwargs):
        """ Reader 工厂方法

        :param market:  std 标准市场, ext 扩展市场
        :param kwargs:
        :return:
        """
        if market == 'ext':
            return ExtReader(**kwargs)

        return StdReader(**kwargs)


class ReaderBase(ABC):
    """股票市场"""

    # 默认通达信安装目录
    tdxdir = 'C:/new_tdx'

    def __init__(self, tdxdir=None):
        """ 构造函数

        :param tdxdir: 通达信安装目录
        """

        if not Path(tdxdir).is_dir():
            raise Exception('tdxdir 目录不存在')

        self.tdxdir = tdxdir

    def find_path(self, symbol=None, subdir='lday', suffix=None):
        """ 自动匹配文件路径，辅助函数

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
            vipdoc = Path(self.tdxdir) / 'vipdoc' / market / subdir / f'{prefix}{symbol}.{ex_}'

            if Path(vipdoc).exists():
                return vipdoc

        return None


class StdReader(ReaderBase):
    """股票市场"""

    def daily(self, symbol=None):
        """ 获取日线数据

        :param symbol:
        :return: pd.dataFrame or None
        """
        reader = MooTdxDailyBarReader()
        vipdoc = self.find_path(symbol=symbol, subdir='lday', suffix='day')

        return reader.get_df(str(vipdoc)) if vipdoc else None

    def minute(self, symbol=None, suffix=1):
        """ 获取1, 5分钟线

        :param suffix:
        :param symbol:
        :return: pd.dataFrame or None
        """
        subdir = 'fzline' if str(suffix) == '5' else 'minline'
        suffix = ['lc5', '5'] if str(suffix) == '5' else ['lc1', '1']
        symbol = self.find_path(symbol, subdir=subdir, suffix=suffix)

        if symbol is not None:
            reader = (TdxMinBarReader() if 'lc' not in symbol.suffix else TdxLCMinBarReader())
            return reader.get_df(str(symbol))

        return None

    def fzline(self, symbol=None):
        """ 分钟线数据

        :param symbol: 自定义板块股票列表, 类型 list
        :return: pd.dataFrame or Bool
        """
        return self.minute(symbol, suffix=5)

    def block_new(self, name: str = None, symbol: list = None, group=False):
        """ 自定义板块数据操作

        提示: name 和 symbol 全为空则为读取，否则写入操作
        参考: http://blog.sina.com.cn/s/blog_623d2d280102vt8y.html

        :param name: 自定义板块名称
        :param symbol: 自定义板块股票列表, 类型 list
        :param group:
        :return: pd.dataFrame or Bool
        """

        if name and symbol:
            return utils.block_new(self.tdxdir, name=name, symbol=symbol)

        vipdoc = Path(self.tdxdir, 'T0002', 'blocknew')
        types_ = TYPE_GROUP if group else TYPE_FLATS

        return CustomerBlockReader().get_df(str(vipdoc), types_) if vipdoc.is_dir() else None

    def block(self, symbol='', group=False):
        """ 获取板块数据

        参考: http://blog.sina.com.cn/s/blog_623d2d280102vt8y.html
        :param symbol: 板块文件名称
        :param group:
        :return: pd.dataFrame or None
        """

        suffix = Path(symbol).suffix
        suffix = suffix if suffix else 'dat'

        symbol = symbol.replace(suffix, '')
        suffix = suffix.strip('.')

        vipdoc = Path(self.tdxdir) / 'T0002' / 'hq_cache' / f'{symbol}.{suffix}'
        types_ = TYPE_GROUP if group else TYPE_FLATS

        return BlockReader().get_df(str(vipdoc), types_) if vipdoc.exists() else None


class ExtReader(ReaderBase):
    """扩展市场读取"""

    def __init__(self, tdxdir=None):
        super(ExtReader, self).__init__(tdxdir)
        self.reader = TdxExHqDailyBarReader()

    def daily(self, symbol=None):
        """ 获取扩展市场日线数据

        :return: pd.dataFrame or None
        """

        vipdoc = self.find_path(symbol=symbol, subdir='lday', suffix='day')
        return self.reader.get_df(str(vipdoc)) if vipdoc else None

    def minute(self, symbol=None):
        """ 获取扩展市场分钟线数据

        :return: pd.dataFrame or None
        """

        if not symbol:
            return None

        vipdoc = self.find_path(symbol=symbol, subdir='minline', suffix=['lc1', '1'])
        return self.reader.get_df(str(vipdoc)) if vipdoc else None

    def fzline(self, symbol=None):
        """ 获取日线数据

        :return: pd.dataFrame or None
        """

        vipdoc = self.find_path(symbol=symbol, subdir='fzline', suffix='lc5')
        return self.reader.get_df(str(vipdoc)) if symbol else None
