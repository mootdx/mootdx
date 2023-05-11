import logging
import os
import warnings
from pathlib import Path

from mootdx import __version__
from mootdx.logger import logger
from mootdx.utils import get_config_path
from mootdx.utils import to_file

try:
    import click
    from prettytable import PrettyTable
except (ImportError, ModuleNotFoundError):
    logging.basicConfig(level=logging.WARNING)
    warnings.warn('!!! 缺少命令行依赖, 请使用次命令进行安装: pip install "mootdx[cli]"', DeprecationWarning)
    logging.warning('!!! 缺少命令行依赖, 请使用次命令进行安装: pip install "mootdx[cli]"')
    exit(-1)


@click.group()
@click.version_option(__version__, '-V', '--version', prog_name='Mootdx', message='%(prog)s: v%(version)s')
@click.help_option('-h', '--help')
def entry():
    ...


@entry.command(help='读取股票在线行情数据.')
@click.help_option('-h', '--help')
@click.option('-o', '--output', default=None, help='输出文件, 支持CSV, HDF5, Excel等格式.')
@click.option('-s', '--symbol', default='600000', help='股票代码.')
@click.option('-a', '--action', default='bars', help='操作类型 (daily: 日线, minute: 一分钟线, fzline: 五分钟线).', )
@click.option('-m', '--market', default='std', help='证券市场, 默认 std (std: 标准股票市场, ext: 扩展市场).')
def quotes(symbol, action, market, output):
    from mootdx.quotes import Quotes

    client = Quotes.factory(market=market, multithread=True)

    try:
        action = 'bars' if 'daily' else action
        if action == 'daily':
            frequency = 9
        elif action == 'minute':
            frequency = 8
        elif action == 'fzline':
            frequency = 0
        else:
            frequency = 9

        feed = getattr(client, 'bars')(symbol=symbol, frequency=frequency)
        to_file(feed, output) if output else None
        click.echo(feed)
    except Exception as e:
        raise e


@entry.command(help='读取股票本地行情数据.')
@click.help_option('-h', '--help')
@click.option('-d', '--tdxdir', default='C:/new_tdx', help='通达信数据目录.')
@click.option('-s', '--symbol', default='600000', help='股票代码.')
@click.option('-a', '--action', default='daily', help='操作类型 (daily: 日线, minute: 一分钟线, fzline: 五分钟线).')
@click.option('-m', '--market', default='std', help='证券市场, 默认 std (std: 标准股票市场, ext: 扩展市场).')
@click.option('-o', '--output', default=None, help='输出文件, 支持 CSV, HDF5, Excel 等格式.')
def reader(symbol, action, market, tdxdir, output):
    from mootdx.reader import Reader

    client = Reader.factory(market=market, tdxdir=tdxdir)

    try:
        feed = getattr(client, action)(symbol=symbol)
        to_file(feed, output) if output else None
        click.echo(feed)
    except Exception as e:
        raise e


@entry.command(help='测试行情服务器.', name='bestip')
@click.help_option('-h', '--help')
@click.option('-l', '--limit', default=5, help='显示最快前几个，默认 5.')
@click.option('-v', '--verbose', count=True, help='详细模式')
def server(limit, verbose):
    from mootdx.server import bestip

    if verbose:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        logger.addHandler(ch)
        logger.setLevel(logging.DEBUG)

    bestip(limit=limit, console=True, sync=False)

    config = get_config_path('config.json')
    logger.info(f'[√] 已经将最优服务器IP写入配置文件 {config}')


@entry.command(help='财务文件下载&解析.')
@click.help_option('-h', '--help')
@click.option('-p', '--parse', default=None, help='要解析文件名')
@click.option('-f', '--fetch', default=None, help='下载财务文件的文件名')
@click.option('-a', '--downall', is_flag=True, help='下载全部文件')
@click.option('-o', '--output', default=None, help='输出文件, 支持 CSV, HDF5, Excel, JSON 等格式.')
@click.option('-d', '--downdir', default='output', help='下载文件目录')
@click.option('-l', '--listfile', is_flag=True, default=False, help='显示全部文件')
@click.option('-v', '--verbose', count=True, help='详细模式')
def affair(parse, fetch, downdir, output, downall, verbose, listfile):
    from mootdx.affair import Affair

    if verbose:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        logger.addHandler(ch)
        logger.setLevel(logging.DEBUG)

    files = Affair.files()

    if listfile:
        t = PrettyTable(['filename', 'filesize', 'hash'])
        t.align['filename'] = 'l'
        t.align['filesize'] = 'l'
        t.align['hash'] = 'l'
        t.padding_width = 0

        for x in files:
            t.add_row([x['filename'], x['filesize'], x['hash']])

        click.echo(t)
        return

    # download all files
    if downall or fetch == 'all':
        feed = Affair.fetch(downdir=downdir)
        return to_file(feed, output) if output else None

    # download file
    if fetch:
        return Affair.fetch(downdir=downdir, filename=fetch.strip('.zip') + '.zip')

    # parse file
    if parse:
        parse = parse.strip('.zip') + '.zip'
        files = [x['filename'] for x in files]

        if parse in files:
            # 文件不存在，先下载
            Path(downdir, parse).exists() or Affair.fetch(downdir=downdir, filename=parse)
            feed = Affair.parse(downdir=downdir, filename=parse)
            output and to_file(feed, output)
            click.echo(feed)
        else:
            logger.error('没找到要解析的文件.')


@entry.command(help='批量下载行情数据.')
@click.help_option('-h', '--help')
@click.option('-o', '--output', default='bundle', help='转存文件目录.')
@click.option('-s', '--symbol', default='600000', help='股票代码. 多个用,隔开')
@click.option('-a', '--action', default='bars', help='操作类型 (daily: 日线, minute: 一分钟线, fzline: 五分钟线).')
@click.option('-m', '--market', default='std', help='证券市场, 默认 std (std: 标准股票市场, ext: 扩展市场).')
@click.option('-e', '--extension', default='csv', help='转存文件的格式, 支持 CSV, HDF5, Excel, JSON 等格式.')
def bundle(symbol, action, market, output, extension):
    """
    批量下载行情数据
    :return:
    """
    from mootdx.quotes import Quotes

    client = Quotes.factory(market=market, multithread=True)
    symbol = symbol.replace('，', ',').strip(',').split(',')

    for code in symbol:
        try:
            if action == 'daily':
                frequency = 9
            elif action == 'minute':
                frequency = 8
            elif action == 'fzline':
                frequency = 0
            else:
                frequency = 9

            feed = getattr(client, 'bars')(symbol=code, frequency=frequency)
            output and to_file(feed, os.path.join(output, f'{code}.{extension}'))
            click.echo('下载完成 {}'.format(code))
        except Exception as e:
            raise e

    click.echo(f'[√] 下载文件到 "{os.path.realpath(output)}"')


if __name__ == '__main__':
    entry()
