from pathlib import Path

import pandas as pd
from loguru import logger
from pytdx.reader import BlockReader

from mootdx.consts import TYPE_FLATS
from mootdx.consts import TYPE_GROUP


# def blocknew(tdxdir: str = None, name: str = None, symbol: list = None, group=False, **kwargs):
#     """
#     自定义板块数据操作
#
#     提示: name 和 symbol 全为空则为读取，否则写入操作
#     参考: http://blog.sina.com.cn/s/blog_623d2d280102vt8y.html
#
#     :param tdxdir: tdx 路径
#     :param name: 自定义板块名称
#     :param symbol: 自定义板块股票列表, 类型 list
#     :param group:
#     :return: pd.dataFrame or Bool
#     """
#
#     if name and symbol:
#         return _blocknew(tdxdir, name=name, symbol=symbol, **kwargs)
#
#     vipdoc = Path(tdxdir, 'T0002', 'blocknew')
#     types_ = TYPE_GROUP if group else TYPE_FLATS
#
#     if not vipdoc.is_dir():
#         return None
#
#     if name:
#         result = CustomerBlockReader().get_df(str(vipdoc), TYPE_GROUP)
#         result = result.loc[result.blockname == name].code_list.values
#         result = list(set(result[0].split(',')))
#     else:
#         result = CustomerBlockReader().get_df(str(vipdoc), types_)
#
#     return result


def block(tdxdir, symbol='', group=False, **kwargs):
    """
    获取板块数据

    参考: http://blog.sina.com.cn/s/blog_623d2d280102vt8y.html

    :param symbol:  板块文件
    :param group:   分组解析
    :return: pd.dataFrame or None
    """

    symbol = Path(symbol).stem
    suffix = Path(symbol).suffix or '.dat'

    vipdoc = (Path('T0002', 'hq_cache'), '')['incon' in symbol]
    vipdoc = Path(tdxdir, vipdoc) / f'{symbol}{suffix}'

    print(str(vipdoc))

    if not vipdoc.exists():
        logger.error(f'文件不存在: {vipdoc}')
        return None

    return BlockReader().get_df(str(vipdoc), (TYPE_FLATS, TYPE_GROUP)[group])


class Parse(object):

    def __init__(self, tdxdir):
        self.tdxdir = tdxdir

    def _incon(self, path):
        t = Path(self.tdxdir, path).read_text(encoding='gbk').strip()
        m = [x for x in t.split('######')]
        v = [n.split() for n in m if n.strip()]
        d = {i[0]: [c.split('|') for c in i[1:]] for i in v}
        d = {key: dict([vv for vv in val if len(vv) == 2]) for key, val in d.items()}

        return d

    def _cfg(self, path):
        ts = Path(self.tdxdir, path).read_text(encoding='gbk').strip()
        ls = [ll.split('|') for ll in ts.split()]
        df = pd.DataFrame(ls)

        return df
