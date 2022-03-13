import time
from datetime import datetime
from pathlib import Path

from loguru import logger
from pytdx.reader import CustomerBlockReader, BlockReader

from mootdx.consts import TYPE_GROUP, TYPE_FLATS
from mootdx.utils import get_stock_market


def _blocknew(tdxdir: str = None, name: str = None, symbol: list = None, blk_file: str = None, **kwargs):
    """
    自定义模块写入函数

    :param tdxdir: tdx 路径
    :param name: 自定义板块名称
    :param symbol: 自定义板块股票代码集合
    :param blk_file: 自定义板块股票代码集合文件
    :return: bool
    """

    if not tdxdir:
        logger.error(f'通达信路径不存在或者空: {tdxdir}')
        return False

    # 自定义板块名称未传入则自动按时间生成名称
    if not name:
        name = datetime.now().strftime('%Y%m%d%H%M%S')

    # 按时间生成 blk 文件名
    blk_file = blk_file if blk_file else str(time.time_ns())

    vipdoc = Path(tdxdir, 'T0002', 'blocknew')
    symbol = list(set(symbol))

    # 判断目录是否存在
    if not Path(vipdoc).is_dir():
        logger.error(f'自定义板块目录错误: {vipdoc}')
        return False

    block_file = Path(vipdoc) / 'blocknew.cfg'

    # 文件不存在就创建
    if not block_file.exists():
        block_file.write_text('')

    # 判断名字是否重名
    with open(block_file, 'rb') as fp:
        names = fp.read().decode('gbk', 'ignore')
        names = names.split('\x00')
        names = [x for x in names if x != '']
        names = [v for i, v in enumerate(names) if i % 2 == 0]

        if name in names:
            # todo symbol 不空则合并, 空则删除
            logger.error('自定义板块名称重复.')
            raise Exception('自定义板块名称重复.')

    # 写 blk 文件
    with open(f'{vipdoc}/{blk_file}.blk', 'w') as fp:
        fp.write('\n'.join([f"{get_stock_market(s)}{s}" for s in symbol]))

    # 写 blocknew.cfg 文件
    with open(block_file, 'ab') as fp:
        data = name + ((50 - len(name.encode('gbk', 'ignore'))) * '\x00')
        data += blk_file + ((70 - len(blk_file.encode('gbk', 'ignore'))) * '\x00')
        data = bytes(data.encode('gbk', 'ignore'))
        fp.write(data)

    return True


def blocknew(tdxdir: str = None, name: str = None, symbol: list = None, group=False, **kwargs):
    """
    自定义板块数据操作

    提示: name 和 symbol 全为空则为读取，否则写入操作
    参考: http://blog.sina.com.cn/s/blog_623d2d280102vt8y.html

    :param name: 自定义板块名称
    :param symbol: 自定义板块股票列表, 类型 list
    :param group:
    :return: pd.dataFrame or Bool
    """

    if name and symbol:
        return _blocknew(tdxdir, name=name, symbol=symbol, **kwargs)

    vipdoc = Path(tdxdir, 'T0002', 'blocknew')
    types_ = TYPE_GROUP if group else TYPE_FLATS

    if not vipdoc.is_dir():
        return None

    if name:
        result = CustomerBlockReader().get_df(str(vipdoc), TYPE_GROUP)
        result = result.loc[result.blockname == name].code_list.values
        result = list(set(result[0].split(',')))
    else:
        result = CustomerBlockReader().get_df(str(vipdoc), types_)

    return result


def block(tdxdir, symbol='', group=False, **kwargs):
    """
    获取板块数据

    参考: http://blog.sina.com.cn/s/blog_623d2d280102vt8y.html

    :param symbol:  板块文件
    :param group:   分组解析
    :return: pd.dataFrame or None
    """

    suffix = Path(symbol).suffix
    suffix = suffix if suffix else 'dat'

    symbol = symbol.replace(suffix, '')
    suffix = suffix.strip('.')

    if 'incon' in symbol:
        vipdoc = Path(tdxdir) / f'{symbol}.{suffix}'
    else:
        vipdoc = Path(tdxdir) / 'T0002' / 'hq_cache' / f'{symbol}.{suffix}'

    vipdoc.exists() or logger.debug(f'文件不存在: {vipdoc}')

    types_ = TYPE_GROUP if group else TYPE_FLATS

    if kwargs.get('debug'):
        return str(vipdoc)

    return BlockReader().get_df(str(vipdoc), types_) if vipdoc.exists() else None
