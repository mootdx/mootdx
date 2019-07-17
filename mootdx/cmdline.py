# -*- coding: utf-8 -*-
"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -m mootdx` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``mootdx.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``mootdx.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

import json
import os

import click

from mootdx.quotes import Quotes
from mootdx.verify import Server


@click.group()
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, verbose):
    ctx.obj["VERBOSE"] = verbose


@cli.command(help='读取股票行情数据.')
@click.option('-o', '--output', default='feed.csv', help='输出文件')
@click.option('-s', '--symbol', default='600001', help='股票代码')
@click.option('-m', '--method', default='bars', help='时间区间')
# @click.option('-m', '--market', default='standard', help='证券市场')
# @click.option('-m', '--market', default='extension', help='证券市场')
def quotes(symbol, method, output):
    client = Quotes()
    feed = getattr(client, method)(symbol=symbol)
    feed.to_csv(output) if output else None

    print(feed)


@cli.command(help='测试行情服务器.')
@click.option('-l', '--limit', default='5', help='显示最快几个')
@click.option('-t', '--tofile', default=None, help='输出文件')
@click.option('-w', '--write', count=True, help='写入配置文件')
@click.option('-v', '--verbose', count=True)
def verify(limit, verbose, write, tofile):
    bestip = Server(limit=int(limit), verbose=verbose, tofile=tofile)
    config = os.path.join(os.environ['HOME'], '.mootdx/config.josn')

    if write:
        if not os.path.exists(config):
            os.mkdir(os.path.join(os.environ['HOME'], '.mootdx'))

        json.dump({'BESTIP': bestip[0]}, open(config, 'w'))


@cli.command(help='财务文件下载&解析.')
@click.option('-p', '--parse', default=None, help='解析文件内容')
@click.option('-l', '--files', count=True, help='列出文件列表')
@click.option('-f', '--fetch', default=None, help='下载全部文件')
@click.option('-o', '--output', default='', help='输出文件')
@click.option('-d', '--downdir', default='tmp', help='下载文件目录')
@click.option('-v', '--verbose', count=True)
def affair(parse, files, fetch, output, downdir, verbose):
    from mootdx.affairs import Affairs
    from prettytable import PrettyTable
    affairs = Affairs.files()

    if files:
        t = PrettyTable(["filename", "filesize", "hash"])
        t.align["filename"] = "l"
        t.align["filesize"] = "l"
        t.align["hash"] = "l"
        t.padding_width = 1

        for x in affairs:
            t.add_row([x['filename'], x['filesize'], x['hash']])

        print(t)

    if fetch:
        if fetch == 'all':
            for x in affairs:
                Affairs.fetch(downdir=downdir, filename=x['filename'])
        else:
            Affairs.fetch(downdir=downdir, filename=fetch.strip('.zip') + '.zip')

    if parse:
        filelist = [x['filename'] for x in affairs]
        if parse in filelist:
            if os.path.exists(os.path.join(downdir, parse)):
                Affairs.parse(downdir=downdir, filename=parse.strip('.zip') + '.zip').to_csv(output)
            else:
                print('file not found.')


def execute():
    cli(obj={})


if __name__ == "__main__":
    execute()
