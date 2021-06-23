# -*- coding: utf-8 -*-
import struct
import tempfile
from urllib.request import Request, urlopen


def reporthook(downloaded, total_size):
    print("Downloaded {}, Total is {}".format(downloaded, total_size))


class BaseReader(object):
    @staticmethod
    def unpack(fmt, data):
        """
        解压文件

        :param fmt:
        :param data:
        :return:
        """

        record = struct.Struct(fmt)
        return (record.unpack_from(data, offset) for offset in range(0, len(data), record.size))

    def get_df(self, code_or_file, exchange=None):
        """
        转换格式为 pd.DateFrame

        :param code_or_file:
        :param exchange:
        :return:
        """

        raise NotImplementedError('not yet')


class BaseFinancial:
    def __init__(self, mode="content"):
        self.mode = mode

    def fetch_and_parse(self, report_hook=None, downdir=None, proxies=None, chunk_size=51200, *args, **kwargs):
        """
        function to get data , 参考 https://docs.python.org/3/library/urllib.request.html#module-urllib.request

        :param report_hook 使用urllib.request 的report_hook 来汇报下载进度
        :param downdir 数据文件下载的地址，如果没有提供，则下载到临时文件中，并在解析之后删除
        :param proxies urllib格式的代理服务器设置
        :param chunk_size chunk_size
        :return: 解析之后的数据结果
        """

        if self.mode == "http":
            file = self.fetch_via_http(report_hook=report_hook, downdir=downdir, proxies=proxies, chunk_size=chunk_size, *args, **kwargs)
        elif self.mode == "content":
            file = self.content(report_hook=report_hook, downdir=downdir, chunk_size=chunk_size, *args, **kwargs)
        else:
            return

        result = self.parse(file, *args, **kwargs)

        try:
            file.close()
        except Exception as e:
            raise e

        return result

    def fetch_via_http(self, report_hook=None, downdir=None, proxies=None, chunk_size=1024 * 50, *args, **kwargs):
        """

        :param report_hook:
        :param downdir:
        :param proxies:
        :param chunk_size:
        :param args:
        :param kwargs:
        :return:
        """

        download_file = open(downdir, 'wb') if downdir else tempfile.NamedTemporaryFile(delete=True)

        url = self.build_url(*args, **kwargs)

        request = Request(url)
        request.add_header('Referer', url)
        request.add_header(
            "User-Agent",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/76.0.3809.100 Safari/537.36 "
        )

        try:
            res = urlopen(request)
        except Exception as e:
            raise e

        if res.getheader('Content-Length') is not None:
            total_size = int(res.getheader('Content-Length').strip())
            downloaded = 0

            while True:
                chunk = res.read(chunk_size)
                downloaded += len(chunk)

                if report_hook is not None:
                    report_hook(downloaded, total_size)

                if not chunk:
                    break

                download_file.write(chunk)
        else:
            content = res.read()
            download_file.write(content)

        download_file.seek(0)
        return download_file

    def build_url(self, *args, **kwargs):
        raise NotImplementedError("will impl in subclass")

    def content(self, report_hook=None, downdir=None, proxies=None, chunk_size=1024 * 50, *args, **kwargs):
        raise NotImplementedError("will impl in subclass")

    def parse(self, download_file, *args, **kwargs):
        raise NotImplementedError("will impl in subclass")
