from pathlib import Path

import pandas as pd
from loguru import logger
from pytdx.reader import BlockReader

from mootdx.consts import TYPE_FLATS
from mootdx.consts import TYPE_GROUP


class BaseParse:
    def __init__(self, tdxdir):
        self.tdxdir = tdxdir

    def parse(self, symbol=None, group=False, **kwargs):
        """
        获取板块数据

        参考: http://blog.sina.com.cn/s/blog_623d2d280102vt8y.html

        :param symbol:  板块文件
        :param group:   分组解析
        :return: pd.dataFrame or None
        """

        suffix = Path(symbol).suffix or '.dat'
        symbol = Path(symbol).stem

        vipdoc = (Path('T0002', 'hq_cache'), '')['incon' in symbol]
        vipdoc = Path(self.tdxdir, vipdoc) / f'{symbol}{suffix}'

        if not vipdoc.exists():
            logger.error(f'文件不存在: {vipdoc}')
            return None

        if 'incon' in symbol:
            return self.__incon(vipdoc)

        if 'block_' in symbol and suffix == '.dat':
            return BlockReader().get_df(str(vipdoc), (TYPE_FLATS, TYPE_GROUP)[bool(group)])

        return self.cfg(vipdoc)

    def read_text(self, path):
        return Path(self.tdxdir, path).read_text(encoding='gbk').strip()

    def __incon(self, path):
        t = self.read_text(path)
        m = [x for x in t.split('######')]
        v = [n.split() for n in m if n.strip()]
        d = {i[0]: [c.split('|') for c in i[1:]] for i in v}
        d = {key: dict([vv for vv in val if len(vv) == 2]) for key, val in d.items()}

        return d

    def cfg(self, path):
        ts = self.read_text(path)
        ls = [ll.split('|') for ll in ts.split()]

        return pd.DataFrame(ls)
