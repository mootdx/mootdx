import time
from datetime import datetime
from pathlib import Path

from tdxpy.reader import CustomerBlockReader

from mootdx.consts import TYPE_FLATS
from mootdx.consts import TYPE_GROUP
from mootdx.logger import logger
from mootdx.utils import get_stock_market

try:
    from time import time_ns
except ImportError:
    # 兼容 3.6
    time_ns = lambda: int(time.time() * 1e9)  # noqa


class Customize:
    items: dict = {}

    def __init__(self, tdxdir=None):
        self.vipdoc = Path(tdxdir, 'T0002', 'blocknew')
        self.tdxdir = str(tdxdir)

    def create(self, name: str = None, symbol: list = None, **kwargs):
        return _blocknew(self.tdxdir, name=name, symbol=symbol, **kwargs)

    def remove(self, name: str = None):
        """
        删除板块数据

        :param name:
        :return:
        """

        block_data = self.search()

        if block_data.empty:
            logger.error('自定义板块数据是空的')
            return

        block_file = Path(self.vipdoc) / 'blocknew.cfg'
        block_temp = block_data[block_data.blockname == name]
        block_type = ''

        # 删除blk文件
        if block_temp.block_type.to_list():
            block_type = list(set(block_temp.block_type.to_list()))[0]
            [
                Path(self.vipdoc, f'{x}.blk').unlink()
                for x in block_temp.block_type.to_list()
                if Path(self.vipdoc, f'{x}.blk').is_file()
            ]

        # 读取文件
        block_data = Path(block_file).read_bytes().decode(encoding='gb2312')

        # 替换内容
        data = name + ((50 - len(name.encode('gbk', 'ignore'))) * '\x00')
        data += block_type + ((70 - len(block_type.encode('gbk', 'ignore'))) * '\x00')
        data = block_data.replace(data, '')
        data = bytes(data.encode('gbk', 'ignore'))

        # 写回文件
        return Path(block_file).write_bytes(data)

    def search(self, name: str = None, group=False):
        """
        按名称查找自定义板块名称

        :param name:
        :param group:
        :return:
        """

        if name:
            result = CustomerBlockReader().get_df(str(self.vipdoc), TYPE_GROUP)
            result = result[result.blockname == name]

            if result.empty:
                return None

            result = result.code_list.values
            result = list(set(result[0].split(',')))

            return result

        # 全部数据
        return CustomerBlockReader().get_df(str(self.vipdoc), (TYPE_FLATS, TYPE_GROUP)[group])

    def update(self, name: str = None, symbol=None, overflow=False):
        """
        修改自定义板块内容

        :param name: 板块名称
        :param symbol: 股票代码, ['600036','600016']
        :param overflow:
        """

        if not name:
            return False

        # 板块路径
        block_path = self.vipdoc
        block_code = list(symbol)

        # 板块数据
        block_data = self.search()
        block_temp = block_data[block_data.blockname == name]

        # 对于名称空的情况, 直接创建写入
        if block_temp.empty:
            logger.debug(f'block_temp is empty {block_temp.empty}')
            return _blocknew(self.tdxdir, name=name, symbol=list(set(symbol)))

        # 覆盖情况
        if not overflow:
            block_code += block_temp.code.to_list()

        # 取 blk 文件名, block_type 不为空
        if block_temp.block_type.to_list():
            block_type = list(set(block_temp.block_type.to_list()))[0]
            logger.debug(f'发现板块文件: {block_type}')
        else:
            # block_type 为空的话
            block_type = datetime.now().strftime('%Y%m%d%H%M%S')
            logger.debug(f'板块文件找不到: {block_type}')

        # 去重股票代码
        block_code = list(set(block_code))
        logger.debug(f'证券代码: {block_code}')

        # 股票代码逗号隔开拼字符串
        block_code = '\n'.join([f'{get_stock_market(s)}{s}' for s in block_code])

        # 写入 blk 文件
        block_file = Path(block_path, f'{block_type}.blk')
        logger.debug(f'写入文件 : {block_file}')

        return block_file.write_text(block_code, encoding='gb2312')


def _blocknew(tdxdir: str = None, name: str = None, symbol: list = None, blk_file: str = None, **kwargs):  # noqa
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
    blk_file = blk_file if blk_file else str(time_ns())

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
        fp.write('\n'.join([f'{get_stock_market(s)}{s}' for s in symbol]))

    # 写 blocknew.cfg 文件
    with open(block_file, 'ab') as fp:
        data = name + ((50 - len(name.encode('gbk', 'ignore'))) * '\x00')
        data += blk_file + ((70 - len(blk_file.encode('gbk', 'ignore'))) * '\x00')

        data = bytes(data.encode('gbk', 'ignore'))
        fp.write(data)

    return True
