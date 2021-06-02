# -*- coding: utf-8 -*-
import logging
import os

from mootdx.financial import financial
from mootdx.utils import TqdmUpTo

logger = logging.getLogger(__name__)


class Affair(object):
    @staticmethod
    def parse(downdir='.', filename=None, *args, **kwargs):
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
            return financial.FinancialReader().to_data(filepath)

        logger.error('文件不存在：{}'.format(filename))
        
        return None

    @staticmethod
    def files():
        '''
        财务文件列表

        :return:
        '''
        history = financial.FinancialList()
        results = history.fetch_and_parse()

        return results

    @staticmethod
    def fetch(downdir='.', filename=None, *args, **kwargs):
        '''
        财务数据下载

        :param downdir:
        :param filename:
        :param kwargs:
        :return:
        '''
        history = financial.FinancialList()
        crawler = financial.Financial()

        if not os.path.isdir(downdir):
            logger.warning('下载目录不存在, 进行创建.')
            os.makedirs(downdir)

        if filename:
            logger.info('下载文件 {}.'.format(filename))
            downfile = os.path.join(downdir, filename)

            with TqdmUpTo(unit='B', unit_scale=True, miniters=1, ascii=True) as t:
                crawler.fetch_and_parse(reporthook=t.update_to, filename=filename, downdir=downfile)

            return True

        list_data = history.fetch_and_parse()

        for x in list_data:
            downfile = os.path.join(downdir, x['filename'])

            # 判断文件存在并且长度一样，则忽略
            if os.path.exists(downfile):
                if int(x.get('filesize')) == int(os.path.getsize(downfile)):
                    logger.warning('[!] 文件已经存在: {} 跳过.'.format(x['filename']))
                    continue

            with TqdmUpTo(unit='b', unit_scale=True, miniters=1, ascii=True) as t:
                logger.warning('\r[+] 准备下载文件 {}.'.format(x['filename']))
                crawler.fetch_and_parse(reporthook=t.update_to, filename=x['filename'], downdir=downfile)
