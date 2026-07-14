import tempfile
import zipfile
from pathlib import Path
from struct import calcsize
from struct import unpack

import pandas as pd
from tdxpy.hq import TdxHq_API

from ..logger import logger
from .base import BaseFinancial
from .columns import columns


class FinancialReader(object):
    @staticmethod
    def to_data(filename, **kwargs):
        """
        读取历史财务数据文件，并返回pandas结果 ， 类似 `gpcw20171231.zip` 格式，具体字段含义参考

        https://github.com/rainx/pytdx/issues/133

        :param filename: 数据文件地址， 数据文件类型可以为 .zip 文件，也可以为解压后的 .dat, 可以不写扩展名. 程序自动识别
        :return: pandas DataFrame 格式的历史财务数据
        """

        crawler = Financial()

        with open(filename, 'rb') as fp:
            data = crawler.parse(download_file=fp)

        return crawler.to_df(data, **kwargs)


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
            download_file = open(downdir, 'wb') if downdir else tmp
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
        if not filename:
            raise ValueError('filename 不能为空')
        filesize = kwargs.get('filesize') or 0

        logger.debug(f'{filename}: start download...')

        api = TdxHq_API()
        api.need_setup = False

        with api.connect(*self.bestip):
            content = api.get_report_file_by_size(f'tdxfin/{filename}', filesize=filesize, reporthook=report_hook)
            if downdir is not None:
                destination = Path(downdir)
                destination.mkdir(parents=True, exist_ok=True)
                download_file = (destination / filename).open('w+b')
            else:
                download_file = tempfile.NamedTemporaryFile(suffix=Path(filename).suffix, delete=True)
            download_file.write(content)
            download_file.seek(0)

            del content

            logger.debug(f'{filename}: done')

            return download_file

    def parse(self, download_file, *args, **kwargs):
        """
        解析财务文件

        :param download_file: 要解析的文件
        :param args:
        :param kwargs:
        :return:
        """

        header_pack_format = '<hIH3L'
        suffix = Path(download_file.name).suffix.lower()
        try:
            if suffix == '.zip':
                with zipfile.ZipFile(download_file) as archive:
                    members = [name for name in archive.namelist() if name.lower().endswith('.dat')]
                    if len(members) != 1:
                        raise ValueError(f'财务压缩包应包含一个 .dat 文件，实际为 {len(members)} 个')
                    payload = archive.read(members[0])
            elif suffix == '.dat':
                download_file.seek(0)
                payload = download_file.read()
            else:
                raise ValueError(f'不支持的财务文件格式: {suffix}')
        finally:
            download_file.close()

        header_size = calcsize(header_pack_format)
        stock_item_format = '<6scL'
        stock_item_size = calcsize(stock_item_format)
        if len(payload) < header_size:
            raise ValueError('财务数据文件头不完整')

        stock_header = unpack(header_pack_format, payload[:header_size])

        max_count = stock_header[2]

        report_date = stock_header[1]
        report_size = stock_header[4]

        report_fields_count = int(report_size / 4)
        report_pack_format = '<{}f'.format(report_fields_count)

        results = []

        for stock_idx in range(0, max_count):
            item_offset = header_size + stock_idx * stock_item_size
            si = payload[item_offset:item_offset + stock_item_size]
            if len(si) != stock_item_size:
                raise ValueError(f'第 {stock_idx} 条证券索引不完整')
            stock_item = unpack(stock_item_format, si)
            code = stock_item[0].decode('ascii', errors='strict').rstrip('\x00')
            info_offset = stock_item[2]
            info_size = calcsize(report_pack_format)
            info_data = payload[info_offset:info_offset + info_size]
            if len(info_data) != info_size:
                raise ValueError(f'{code} 的财务记录不完整')
            cw_info = unpack(report_pack_format, info_data)
            one_record = (code, report_date) + cw_info
            results.append(one_record)

        return results

    @staticmethod
    def to_df(data, header='zh'):
        """
        转换数据为 pandas DataFrame 格式

        :param data: 要转换的数据
        :param header: 是否中文表头
        :return: DataFrame
        """

        if len(data) == 0 or len(data[0]) == 0:
            return pd.DataFrame(data=None)

        column = ['code', 'report_date']

        for i in range(1, len(data[0]) - 1):
            column.append('col' + str(i))

        df = pd.DataFrame(data=data, columns=column).set_index('code')

        if header == 'zh':
            labels = list(columns)
            if len(labels) < len(df.columns):
                labels.extend(df.columns[len(labels):])
            df.columns = labels[:len(df.columns)]

        logger.debug(df.shape)

        return df
