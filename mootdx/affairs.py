# -*- coding: utf-8 -*-
import logging
import os

from pytdx.crawler.base_crawler import demo_reporthook
from pytdx.crawler.history_financial_crawler import (HistoryFinancialCrawler,
                                                     HistoryFinancialListCrawler)
from pytdx.reader.history_financial_reader import HistoryFinancialReader
from tqdm import tqdm

logger = logging.getLogger(__name__)


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
        return Affairs.fetch(filelist=True)

    # 财务数据下载
    @staticmethod
    def fetch(downdir='.', filename=None, filelist=False, **kwargs):
        history = HistoryFinancialListCrawler()
        list_data = history.fetch_and_parse()

        if filelist:
            logger.debug(filelist)
            return list_data

        crawler = HistoryFinancialCrawler()

        if not os.path.isdir(downdir):
            logger.debug('下载目录不存在, 进行创建.')
            os.makedirs(downdir)

        if filename:
            logger.debug('下载文件 {}.'.format(filename))
            downfile = os.path.join(downdir, filename)
            crawler.fetch_and_parse(reporthook=demo_reporthook, filename=filename, path_to_download=downfile)
            return list_data

        for x in tqdm(list_data):
            logger.debug('下载多文件 {}.'.format(x['filename']))
            downfile = os.path.join(downdir, x['filename'])
            result = crawler.fetch_and_parse(reporthook=demo_reporthook, filename=x['filename'],
                                             path_to_download=downfile)

        return list_data
