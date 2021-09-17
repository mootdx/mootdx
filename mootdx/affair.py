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
    result = await asyncio.get_event_loop().run_in_executor(None, partial(financial.Financial().fetch_only, report_hook=None, filename=filename, downdir=downdir))
    return result


class Affair(object):
    @staticmethod
    def parse(downdir='.', filename=None):
        """ 按目录解析文件

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
        """ 财务文件列表

        :return: object
        """

        return financial.FinancialList().fetch_and_parse()

    @staticmethod
    def fetch(downdir='.', filename=None):
        """ 财务数据下载

        :param downdir: 下载路径
        :param filename: 文件名
        :return:
        """

        history = financial.FinancialList()
        crawler = financial.Financial()

        if not Path(downdir).is_dir():
            log.warning('下载目录不存在, 进行创建.')
            Path(downdir).mkdir(parents=True)

        if filename:
            log.info('下载文件 {}.'.format(filename))
            crawler.fetch_only(report_hook=None, filename=filename, downdir=downdir)
            return True

        list_data = history.fetch_and_parse()
        tasks = []

        loop = asyncio.get_event_loop()

        for x in list_data:
            task = loop.create_task(fetch_file(filename=x['filename'], downdir=downdir))
            tasks.append(task)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
