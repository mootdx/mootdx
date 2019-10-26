# -*- coding: utf-8 -*-
import logging
import struct
import tempfile
from urllib.request import Request, urlopen

import requests

logger = logging.getLogger(__name__)


def reporthook(downloaded, total_size):
    print("Downloaded {}, Total is {}".format(downloaded, total_size))


class BaseReader(object):

    def unpack(self, format, data):
        record = struct.Struct(format)
        return (record.unpack_from(data, offset) for offset in range(0, len(data), record.size))

    def get_df(self, code_or_file, exchange=None):
        raise NotImplementedError('not yet')


class BaseFinancial:

    def __init__(self, mode="http"):
        self.mode = "http"

    def fetch_and_parse(self, reporthook=None, downdir=None, proxies=None, chunksize=1024 * 50, *args,
                        **kwargs):
        """
        function to get data ,
        :param reporthook 使用urllib.request 的report_hook 来汇报下载进度 \
                    参考 https://docs.python.org/3/library/urllib.request.html#module-urllib.request
        :param downdir 数据文件下载的地址，如果没有提供，则下载到临时文件中，并在解析之后删除
        :param proxies urllib格式的代理服务器设置
        :return: 解析之后的数据结果
        """

        if self.mode == "http":
            download_file = self.fetch_via_http(reporthook=reporthook, downdir=downdir,
                                                proxies=proxies, chunksize=chunksize, *args, **kwargs)
        elif self.mode == "content":
            download_file = self.get_content(reporthook=reporthook, downdir=downdir,
                                             chunksize=chunksize, *args, **kwargs)
        else:
            return

        result = self.parse(download_file, *args, **kwargs)

        try:
            download_file.close()
        except Exception as e:
            raise e

        return result

    def fetch_via_http(self, reporthook=None, downdir=None, proxies=None, chunksize=1024 * 50, *args,
                       **kwargs):
        if downdir is None:
            download_file = tempfile.NamedTemporaryFile(delete=True)
        else:
            download_file = open(downdir, 'wb')

        url = self.get_url(*args, **kwargs)

        logger.debug(url)

        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            'Referer': url
        }

        res = requests.get(url, headers=headers)

        request = Request(url)
        request.add_header('Referer', url)
        request.add_header('User-Agent',
                           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36")

        res = urlopen(request)

        if res.getheader('Content-Length') is not None:
            total_size = int(res.getheader('Content-Length').strip())
            downloaded = 0

            while True:
                chunk = res.read(chunksize)
                downloaded += len(chunk)

                if reporthook is not None:
                    reporthook(downloaded, total_size)

                if not chunk:
                    break

                download_file.write(chunk)
        else:
            content = res.read()
            download_file.write(content)

        download_file.seek(0)
        return download_file

    def get_url(self, *args, **kwargs):
        raise NotImplementedError("will impl in subclass")

    def get_content(self, reporthook=None, downdir=None, proxies=None, chunksize=1024 * 50, *args, **kwargs):
        raise NotImplementedError("will impl in subclass")

    def parse(self, download_file, *args, **kwargs):
        raise NotImplementedError("will impl in subclass")
