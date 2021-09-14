import asyncio
from functools import partial
from pathlib import Path

from mootdx.financial import financial
from mootdx.logger import log
from mootdx.utils import TqdmUpTo


def download(downdir, filename):
    with TqdmUpTo(unit='B', unit_scale=True, miniters=1, ascii=True) as t:
        financial.Financial().fetch_and_parse(report_hook=t.update_to, filename=filename, downdir=downdir)

    return True


async def fetch_file(downdir, filename):
    result = await asyncio.get_event_loop().run_in_executor(None, partial(financial.Financial().fetch_and_parse, report_hook=None, filename=filename, downdir=downdir))
    return result


class Affair(object):
    @staticmethod
    def parse(downdir='.', filename=None):
        """
        按目录解析文件

        :param downdir:
        :param filename:
        :return:
        """

        if not filename:
            log.critical('文件名不能为空!')
            return None

        filepath = Path(downdir) / filename

        if Path(filepath).exists():
            return financial.FinancialReader().to_data(filepath)

        log.warning('文件不存在：{}'.format(filename))

        return None

    @staticmethod
    def files():
        """
        财务文件列表

        :return:
        """

        history = financial.FinancialList()
        results = history.fetch_and_parse()

        return results

    @staticmethod
    def fetch(downdir='.', filename=None):
        """
        财务数据下载

        :param downdir:
        :param filename:
        :return:
        """

        history = financial.FinancialList()
        crawler = financial.Financial()

        if not Path(downdir).is_dir():
            log.warning('下载目录不存在, 进行创建.')
            Path(downdir).mkdir(parents=True)

        if filename:
            log.info('下载文件 {}.'.format(filename))
            downfile = Path(downdir, filename)

            with TqdmUpTo(unit='B', unit_scale=True, miniters=1, ascii=True) as t:
                crawler.fetch_and_parse(report_hook=t.update_to, filename=filename, downdir=downdir)

            return True

        list_data = history.fetch_and_parse()
        tasks = []
        loop = asyncio.get_event_loop()

        for x in list_data:
            task = loop.create_task(fetch_file(filename=x['filename'], downdir=downdir))
            tasks.append(task)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
    #
    #     for x in list_data:
    #         downfile = Path(downdir, x["filename"])
    #
    #         # 判断文件存在并且长度一样，则忽略
    #         if Path(downfile).exists():
    #             if int(x.get("filesize")) == int(Path(downfile).stat().st_size):
    #                 log.warning("[!] 文件已经存在: {} 跳过.".format(x["filename"]))
    #                 continue
    #
    #         with TqdmUpTo(unit="b", unit_scale=True, miniters=1, ascii=True) as t:
    #             print("\r[+] 准备下载文件 {}.".format(x["filename"]))
    #             crawler.fetch_and_parse(report_hook=t.update_to, filename=x["filename"], downdir=downfile)
    #
    # def async_fetch(self, downdir=".", filename=None):
    #     loop = asyncio.get_event_loop()
    #
    #     tasks = []
    #     history = financial.FinancialList()
    #     list_data = history.fetch_and_parse()
    #
    #     for x in list_data:
    #         downfile = Path(downdir, x["filename"])
    #         task = loop.create_task(partial(self.fetch(downdir=".", filename=downfile)))
    #         tasks.append(task)
    #
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(asyncio.wait(tasks))
