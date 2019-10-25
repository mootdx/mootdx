# -*- coding: utf-8 -*-
import logging
import os

from pytdx.crawler.history_financial_crawler import (HistoryFinancialCrawler,
                                                     HistoryFinancialListCrawler)
from pytdx.reader.history_financial_reader import HistoryFinancialReader

logger = logging.getLogger(__name__)


def reporthook(downloaded, total_size):
    logger.debug("Downloaded {}, Total is {}".format(downloaded, total_size))


# 股票市场
class Affairs(object):
    @staticmethod
    def parse(downdir='.', filename=None, **kwargs):
        filepath = os.path.join(downdir, filename)

        if os.path.exists(filepath):
            result = HistoryFinancialReader().get_df(filepath)
            return result

        logger.error('文件不存在：{}'.format(filename))
        return None

    @staticmethod
    def files():
        history = HistoryFinancialListCrawler()
        results = history.fetch_and_parse()

        return results

    # 财务数据下载
    @staticmethod
    def fetch(downdir='.', filename=None, **kwargs):
        history = HistoryFinancialListCrawler()
        crawler = HistoryFinancialCrawler()

        if not os.path.isdir(downdir):
            logger.debug('下载目录不存在, 进行创建.')
            os.makedirs(downdir)

        if filename:
            logger.debug('下载文件 {}.'.format(filename))
            downfile = os.path.join(downdir, filename)
            crawler.fetch_and_parse(reporthook=reporthook, filename=filename, path_to_download=downfile)
            return True

        list_data = history.fetch_and_parse()

        for x in list_data:
            logger.debug('下载多文件 {}.'.format(x['filename']))
            downfile = os.path.join(downdir, x['filename'])
            crawler.fetch_and_parse(reporthook=reporthook, filename=x['filename'], path_to_download=downfile)

        return True
