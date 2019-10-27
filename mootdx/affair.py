# -*- coding: utf-8 -*-
import logging
import os

from mootdx.financial.financial import FinancialList, Financial, FinancialReader

logger = logging.getLogger(__name__)


def reporthook(downloaded, total_size):
    logger.debug("\rDownloaded {}, Total is {}".format(downloaded, total_size))


class Affair(object):
    @staticmethod
    def parse(downdir='.', filename=None, **kwargs):
        filepath = os.path.join(downdir, filename)

        if os.path.exists(filepath):
            result = FinancialReader().get_df(filepath)
            return result

        logger.error('文件不存在：{}'.format(filename))
        return None

    @staticmethod
    def files():
        history = FinancialList()
        results = history.fetch_and_parse()

        return results

    # 财务数据下载
    @staticmethod
    def fetch(downdir='.', filename=None, **kwargs):
        history = FinancialList()
        crawler = Financial()

        if not os.path.isdir(downdir):
            logger.info('\r下载目录不存在, 进行创建.')
            os.makedirs(downdir)

        list_data = history.fetch_and_parse()

        if filename:
            logger.info('\r下载文件 {}.'.format(filename))
            downfile = os.path.join(downdir, filename)
            crawler.fetch_and_parse(reporthook=reporthook, filename=filename, downdir=downfile)
            return True

        for x in list_data:
            logger.debug('\r下载多文件 {}.'.format(x['filename']))
            downfile = os.path.join(downdir, x['filename'])

            if os.path.exists(downfile):
                if x.get('filesize') == os.path.getsize(downfile):
                    logger.warning('\r文件已经存在: {} 跳过.'.format(x['filename']))
                    continue

            crawler.fetch_and_parse(reporthook=reporthook, filename=x['filename'], downdir=downfile)
