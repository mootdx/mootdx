# -*- coding: utf-8 -*-
# @Author  : BoPo
# @Time    : 2022/2/17 14:49
# @Function:
from datetime import datetime
from pathlib import Path

from pytdx.reader import CustomerBlockReader

from .. import utils
from ..consts import TYPE_GROUP, TYPE_FLATS
from ..logger import logger
from ..utils import get_stock_market


class Customize:
    items: dict = {}

    def __init__(self, tdxdir=None):
        self.vipdoc = Path(tdxdir, 'T0002', 'blocknew')
        self.tdxdir = str(tdxdir)

    def create(self, name: str = None, symbol: list = None, **kwargs):
        return utils.block_new(self.tdxdir, name=name, symbol=symbol, **kwargs)

    def remove(self, name: str):
        # 板块数据
        block_data = self.search()
        block_file = Path(self.vipdoc) / 'blocknew.cfg'
        block_temp = block_data[block_data.blockname == name]
        block_type = ''

        if block_temp.block_type.to_list():
            block_type = list(set(block_temp.block_type.to_list()))[0]
            [Path(self.vipdoc, f"{x}.blk").unlink() for x in block_temp.block_type.to_list() if Path(self.vipdoc, f"{x}.blk").is_file()]

        block_data = Path(block_file).read_bytes().decode(encoding='gb2312')
        data = name + ((50 - len(name.encode('gbk', 'ignore'))) * '\x00')
        data += block_type + ((70 - len(block_type.encode('gbk', 'ignore'))) * '\x00')
        data = block_data.replace(data, '')
        data = bytes(data.encode('gbk', 'ignore'))

        return Path(block_file).write_bytes(data)

    def search(self, name: str = None, group=None):
        types_ = TYPE_GROUP if group else TYPE_FLATS

        if name:
            result = CustomerBlockReader().get_df(str(self.vipdoc), TYPE_GROUP)
            result = result.loc[result.blockname == name]

            if result.empty:
                return None

            result = result.code_list.values
            result = list(set(result[0].split(',')))
        else:
            result = CustomerBlockReader().get_df(str(self.vipdoc), types_)

        return result

    def update(self, name, symbol=None, overflow=False):
        """
        修改自定义板块内容

        :param name: 板块名称
        :param symbol: 股票代码, ['600036','600016']
        :param overflow:
        """

        # 板块路径
        block_path = self.vipdoc
        block_code = list(symbol)

        # 板块数据
        block_data = self.search()
        block_temp = block_data[block_data.blockname == name]

        # 对于名称空的情况, 直接创建写入
        if block_temp.empty:
            logger.debug('block_temp is empty {}', block_temp.empty)
            return utils.block_new(self.tdxdir, name=name, symbol=list(set(symbol)))

        # 覆盖情况
        if not overflow:
            block_code += block_temp.code.to_list()

        # 取 blk 文件名, block_type 不为空
        if block_temp.block_type.to_list():
            block_type = list(set(block_temp.block_type.to_list()))[0]
            logger.debug('发现板块文件: {}', block_type)
        else:
            # block_type 为空的话
            block_type = datetime.now().strftime('%Y%m%d%H%M%S')
            logger.debug('板块文件找不到: {}', block_type)

        # 去重股票代码
        block_code = list(set(block_code))
        logger.debug('证券代码: {}', block_code)

        # 股票代码逗号隔开拼字符串
        block_code = '\n'.join([f"{get_stock_market(s)}{s}" for s in block_code])

        # 写入 blk 文件
        logger.debug("写入文件 : {}", Path(block_path, f"{block_type}.blk"))
        return Path(block_path, f"{block_type}.blk").write_text(block_code, encoding='gb2312')
