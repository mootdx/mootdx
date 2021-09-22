import os
import random
import shutil
import tempfile
from pathlib import Path
from struct import calcsize
from struct import unpack

import pandas as pd
from pytdx.hq import TdxHq_API

from .base import BaseFinancial
from ..logger import log
from ..logger import logger


class FinancialReader(object):
    @staticmethod
    def to_data(filename):
        """
        读取历史财务数据文件，并返回pandas结果 ， 类似 `gpcw20171231.zip` 格式，具体字段含义参考

        https://github.com/rainx/pytdx/issues/133

        :param filename: 数据文件地址， 数据文件类型可以为 .zip 文件，也可以为解压后的 .dat, 可以不写扩展名. 程序自动识别
        :return: pandas DataFrame 格式的历史财务数据
        """

        crawler = Financial()

        with open(filename, 'rb') as fp:
            data = crawler.parse(download_file=fp)

        return crawler.to_df(data)


class FinancialList(BaseFinancial):

    def content(self, report_hook=None, downdir=None, proxies=None, chunk_size=1024 * 50, *args, **kwargs):
        """
        解析财务文件

        :param report_hook: 钩子回调函数
        :param downdir: 要解析的文件夹
        :param proxies:
        :param chunk_size:
        :param args:
        :param kwargs:
        :return:
        """

        tmp = tempfile.NamedTemporaryFile(delete=True)

        api = TdxHq_API(**kwargs)
        api.need_setup = False

        with api.connect(*self.bestip):
            content = api.get_report_file_by_size('tdxfin/gpcw.txt')
            download_file = (open(downdir, 'wb') if downdir else tmp)
            download_file.write(content)
            download_file.seek(0)

            return download_file

    def parse(self, download_file, *args, **kwargs):
        """
        解析财务文件

        :param download_file:
        :param args:
        :param kwargs:
        :return:
        """

        with download_file:
            content = download_file.read()
            content = content.decode('utf-8')

        def l2d(i):
            return {'filename': i[0], 'hash': i[1], 'filesize': int(i[2])}

        if content:
            content = content.strip().split('\n')
            return [l2d(i) for i in [line.strip().split(',') for line in content]]

        return None


class Financial(BaseFinancial):

    def content(self, report_hook=None, downdir=None, proxies=None, chunk_size=51200, *args, **kwargs):
        """
        解析财务文件

        :param report_hook: 钩子回调函数
        :param downdir: 要解析的文件夹
        :param proxies: 代理配置
        :param chunk_size:
        :param args:
        :param kwargs:
        :return:
        """

        filename = kwargs.get('filename')
        downfile = str(Path(downdir) / filename)
        filesize = kwargs.get('filesize') if kwargs.get('filesize') else 0

        log.info('{}: start download...', filename)

        if not filename:
            raise Exception('Param filename is not set')

        api = TdxHq_API()
        api.need_setup = False

        with api.connect(*self.bestip):
            content = api.get_report_file_by_size(f'tdxfin/{filename}', filesize=filesize, reporthook=report_hook)
            download_file = (open(downfile, 'wb') if downfile else tempfile.NamedTemporaryFile(delete=True))
            download_file.write(content)
            download_file.seek(0)

            del content

            log.info('{}: done', filename)

            return download_file

    def parse(self, download_file, *args, **kwargs):
        """
        解析财务文件

        :param download_file: 要解析的文件
        :param args:
        :param kwargs:
        :return:
        """

        header_pack_format = '<1hI1H3L'
        tmpdir = tempfile.gettempdir()

        if download_file.name.endswith('.zip'):
            tmpdir_root = tempfile.gettempdir()
            random_sums = str(random.randint(0, 1000000))
            subdir_name = f'mootdx_{random_sums}'

            tmpdir = Path(tmpdir_root, subdir_name)
            shutil.rmtree(tmpdir, ignore_errors=True)
            Path(tmpdir).mkdir(parents=True)

            shutil.unpack_archive(download_file.name, extract_dir=tmpdir)

            # only one file endswith .dat should be in zip archives
            datfile = None

            for _file in os.listdir(tmpdir):
                if _file.endswith('.dat'):
                    datfile = open(Path(tmpdir, _file), 'rb')

            if datfile is None:
                raise Exception('no dat file found in zip archive')

        elif download_file.name.endswith('.dat'):
            datfile = download_file
        else:
            return None

        header_size = calcsize(header_pack_format)
        stock_item_size = calcsize('<6s1c1L')
        data_header = datfile.read(header_size)
        stock_header = unpack(header_pack_format, data_header)

        max_count = stock_header[2]

        report_date = stock_header[1]
        report_size = stock_header[4]

        report_fields_count = int(report_size / 4)
        report_pack_format = '<{}f'.format(report_fields_count)

        results = []

        for stock_idx in range(0, max_count):
            datfile.seek(header_size + stock_idx * calcsize('<6s1c1L'))
            si = datfile.read(stock_item_size)
            stock_item = unpack('<6s1c1L', si)
            code = stock_item[0].decode('utf-8')
            datfile.seek(stock_item[2])

            info_data = datfile.read(calcsize(report_pack_format))
            cw_info = unpack(report_pack_format, info_data)
            one_record = (code, report_date) + cw_info
            results.append(one_record)

        if download_file.name.endswith('.zip'):
            datfile.close()
            shutil.rmtree(tmpdir, ignore_errors=True)

        download_file.close()

        return results

    @staticmethod
    def to_df(data):
        """
        转换数据为 pandas DataFrame 格式
        :param data: 要转换的数据
        :return: DataFrame
        """

        if len(data) == 0 or len(data[0]) == 0:
            return None

        length = len(data[0]) - 1
        column = ['code', 'report_date']

        for i in range(1, length):
            column.append('col' + str(i))

        df = pd.DataFrame(data=data, columns=column)
        df.set_index('code', inplace=True)

        logger.debug(df)

        return df
