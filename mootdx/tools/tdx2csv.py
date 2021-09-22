import asyncio
import glob
from functools import partial
from pathlib import Path

import pandas as pd

from mootdx.logger import log


def txt2csv(infile: str, outfile: str = None) -> pd.DataFrame:
    """ 通达信导出文件转换为 Pandas 可用的 csv 文件

    :param infile: 通达信导出的 txt 文件路径
    :param outfile: 转换后的目标 csv 文件路径
    """

    try:
        names = ['date', 'open', 'high', 'low', 'close', 'volume', 'amount']
        df = pd.read_csv(infile, names=names, header=2, skipfooter=1, index_col='date', engine='python')

        # 传参 outfile 目录存在则写文件
        Path(outfile).parent.is_dir() and df.to_csv(outfile)

        return df
    except FileNotFoundError as ex:
        log.exception(ex)
        log.warning(f'输入文件不存在: {infile}')
        raise ex
    except ValueError as ex:
        log.warning(f'无法解析输入文件: {infile}')
        raise ex


async def covert(src, dst):
    log.info('covert...')
    return await asyncio.get_event_loop().run_in_executor(None, partial(txt2csv, src=src, dst=dst))


def batch(src, dst):
    """ 批量转换通达信导出文件

    :param src: 来源目录
    :param dst: 目标目录
    """

    tasks = []
    event = asyncio.get_event_loop()

    # 分配任务
    for x in glob.glob1(src, '*.txt'):
        src = str(Path(src, x))
        dst = str(Path(dst, x.replace('.txt', '.csv')))

        task = event.create_task(partial(covert, src=src, dst=dst))
        tasks.append(task)

    # 执行任务
    event.run_until_complete(asyncio.wait(tasks))


__all__ = ('txt2csv', 'batch')
