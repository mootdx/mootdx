# -*- coding: utf-8 -*-
import logging
import os
import random
import shutil
import tempfile
from struct import calcsize, unpack

import pandas as pd

from mootdx.consts import gp_hosts
from .base import BaseFinancial, BaseReader

logger = logging.getLogger(__name__)


class FinancialReader(BaseReader):

    def get_df(self, filename, **kwargs):
        """
        读取历史财务数据文件，并返回pandas结果 ， 类似gpcw20171231.zip格式，具体字段含义参考

        https://github.com/rainx/pytdx/issues/133

        :param **kwargs:
        :param filename: 数据文件地址， 数据文件类型可以为 .zip 文件，也可以为解压后的 .dat, 可以不写扩展名. 程序自动识别
        :return: pandas DataFrame格式的历史财务数据
        """

        crawler = Financial()

        with open(filename, 'rb') as df:
            data = crawler.parse(download_file=df)

        return crawler.to_df(data)


class FinancialList(BaseFinancial):

    def __init__(self):
        super().__init__()
        self.mode = "content"

    def get_url(self, *args, **kwargs):
        return 'http://down.tdx.com.cn:8001/fin/gpcw.txt'
        # return "https://gitee.com/yutiansut/QADATA/raw/master/financial/content.txt"

    def get_content(self, reporthook=None, downdir=None, proxies=None, chunksize=1024 * 50, *args, **kwargs):
        from pytdx.hq import TdxHq_API
        api = TdxHq_API()
        api.need_setup = False
        # calc.tdx.com.cn, calc2.tdx.com.cn
        with api.connect(ip=gp_hosts[0]):
            content = api.get_report_file_by_size("tdxfin/gpcw.txt")

            if downdir is None:
                download_file = tempfile.NamedTemporaryFile(delete=True)
            else:
                download_file = open(downdir, 'wb')

            download_file.write(content)
            download_file.seek(0)

            return download_file

    def parse(self, download_file, *args, **kwargs):
        content = download_file.read()
        content = content.decode("utf-8")

        def list_to_dict(l):
            return {'filename': l[0], 'hash': l[1], 'filesize': int(l[2])}

        if content:
            result = [list_to_dict(l) for l in [line.strip().split(",") for line in content.strip().split('\n')]]
            return result

        return None


class Financial(BaseFinancial):

    def __init__(self):
        super().__init__()
        self.mode = "content"

    def get_url(self, *args, **kwargs):
        if 'filename' in kwargs:
            filename = kwargs['filename']
        else:
            raise Exception("Param filename is not set")

        return "http://data.yutiansut.com/{}".format(filename)

    def get_content(self, reporthook=None, downdir=None, proxies=None, chunksize=1024 * 50, *args, **kwargs):
        if 'filename' in kwargs:
            filename = kwargs['filename']
        else:
            raise Exception("Param filename is not set")

        if "filesize" in kwargs:
            filesize = kwargs["filesize"]
        else:
            filesize = 0

        from pytdx.hq import TdxHq_API

        api = TdxHq_API()
        api.need_setup = False

        # calc.tdx.com.cn, calc2.tdx.com.cn
        with api.connect(ip=gp_hosts[0]):
            content = api.get_report_file_by_size("tdxfin/" + filename, filesize=filesize, reporthook=reporthook)

            if downdir is None:
                download_file = tempfile.NamedTemporaryFile(delete=True)
            else:
                download_file = open(downdir, 'wb')

            download_file.write(content)
            download_file.seek(0)

            return download_file

    def parse(self, download_file, *args, **kwargs):

        header_pack_format = '<1hI1H3L'
        tmpdir = tempfile.gettempdir()

        if download_file.name.endswith('.zip'):
            tmpdir_root = tempfile.gettempdir()
            subdir_name = "mootdx_{}".format(str(random.randint(0, 1000000)))

            tmpdir = os.path.join(tmpdir_root, subdir_name)
            shutil.rmtree(tmpdir, ignore_errors=True)
            os.makedirs(tmpdir)
            shutil.unpack_archive(download_file.name, extract_dir=tmpdir)

            # only one file endswith .dat should be in zip archives
            datfile = None

            for _file in os.listdir(tmpdir):
                if _file.endswith(".dat"):
                    datfile = open(os.path.join(tmpdir, _file), "rb")

            if datfile is None:
                raise Exception("no dat file found in zip archive")
        else:
            datfile = download_file

        header_size = calcsize(header_pack_format)
        stock_item_size = calcsize("<6s1c1L")
        data_header = datfile.read(header_size)
        stock_header = unpack(header_pack_format, data_header)

        max_count = stock_header[2]

        report_date = stock_header[1]
        report_size = stock_header[4]
        report_fields_count = int(report_size / 4)
        report_pack_format = '<{}f'.format(report_fields_count)
        results = []

        for stock_idx in range(0, max_count):
            datfile.seek(header_size + stock_idx * calcsize("<6s1c1L"))
            si = datfile.read(stock_item_size)
            stock_item = unpack("<6s1c1L", si)
            code = stock_item[0].decode("utf-8")
            foa = stock_item[2]
            datfile.seek(foa)

            info_data = datfile.read(calcsize(report_pack_format))
            cw_info = unpack(report_pack_format, info_data)
            one_record = (code, report_date) + cw_info
            results.append(one_record)

        if download_file.name.endswith('.zip'):
            datfile.close()
            shutil.rmtree(tmpdir, ignore_errors=True)

        return results

    def to_df(self, data):
        if len(data) == 0:
            return None

        total_lengh = len(data[0])
        col = ['code', 'report_date']
        length = total_lengh - 2

        for i in range(0, length):
            col.append("col" + str(i + 1))

        df = pd.DataFrame(data=data, columns=col)
        df.set_index('code', inplace=True)

        return df
