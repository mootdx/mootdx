# -*- coding: utf-8 -*-
import logging

from mootdx.financial.financial import FinancialList, Financial, FinancialReader

logger = logging.getLogger(__name__)
total = 0
pbar = None

import os
from tqdm import tqdm


class TqdmUpTo(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""

    def update_to(self, downloaded=0, total_size=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if total_size is not None:
            self.total = total_size

        # self.ascii = True
        self.update(downloaded - self.n)  # will also set self.n = b * bsize


class Affair(object):
    @staticmethod
    def parse(downdir='.', filename=None, **kwargs):
        '''
        按目录解析文件

        :param downdir:
        :param filename:
        :param kwargs:
        :return:
        '''
        filepath = os.path.join(downdir, filename)

        logger.debug(filepath)

        if os.path.exists(filepath):
            result = FinancialReader().to_data(filepath)
            return result

        logger.error('文件不存在：{}'.format(filename))
        return None

    @staticmethod
    def files():
        '''
        财务文件列表

        :return:
        '''
        history = FinancialList()
        results = history.fetch_and_parse()

        return results

    @staticmethod
    def fetch(downdir='.', filename=None, **kwargs):
        '''
        财务数据下载

        :param downdir:
        :param filename:
        :param kwargs:
        :return:
        '''
        history = FinancialList()
        crawler = Financial()

        if not os.path.isdir(downdir):
            logger.info('\r下载目录不存在, 进行创建.')
            os.makedirs(downdir)

        if filename:
            logger.info('\r下载文件 {}.'.format(filename))
            downfile = os.path.join(downdir, filename)

            with TqdmUpTo(unit='B', unit_scale=True, miniters=1) as t:
                crawler.fetch_and_parse(reporthook=t.update_to, filename=filename, downdir=downfile)

            return True

        list_data = history.fetch_and_parse()

        for x in list_data:
            downfile = os.path.join(downdir, x['filename'])

            # 判断文件存在并且长度一样，则忽略
            if os.path.exists(downfile):
                if int(x.get('filesize')) == int(os.path.getsize(downfile)):
                    logger.warning('\r文件已经存在: {} 跳过.'.format(x['filename']))
                    continue

            with TqdmUpTo(unit='b', unit_scale=True, miniters=1) as t:
                logger.debug('\r准备下载多文件 {}.'.format(x['filename']))
                crawler.fetch_and_parse(reporthook=t.update_to, filename=x['filename'], downdir=downfile)
