# -*- coding: utf-8 -*-
import os

from pytdx.crawler.base_crawler import demo_reporthook
from pytdx.crawler.history_financial_crawler import (HistoryFinancialCrawler,
                                                     HistoryFinancialListCrawler)
from pytdx.reader import HistoryFinancialReader


# 股票市场
class Affairs(object):
    @staticmethod
    def parse(downdir='.', filename=None, **kwargs): 
        filepath = os.path.join(downdir, filename)
        result = HistoryFinancialReader().get_df(filepath)
        
        return result


    @staticmethod
    def files():
        return Affairs.fetch(filelist=True)
        
    # 财务数据下载
    @staticmethod
    def fetch(downdir='.', filename=None, filelist=False, **kwargs):
        crawler = HistoryFinancialListCrawler()
        list_data = crawler.fetch_and_parse()
        
        if filelist:
            return list_data

        datacrawler = HistoryFinancialCrawler()

        if filename:
            downfile = os.path.join(downdir, filename)
            datacrawler.fetch_and_parse(reporthook=demo_reporthook, filename=filename, path_to_download=downfile)
            return list_data
            
        for x in list_data:
            downfile = os.path.join(downdir, x['filename'])
            result = datacrawler.fetch_and_parse(reporthook=demo_reporthook, filename=x['filename'], path_to_download=downfile)

        return list_data
