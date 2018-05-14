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
import logging
import re
import socket
import threading
import time

import click
import coloredlogs
from prettytable import PrettyTable
from mootdx.verify import check
from mootdx.quotes import Quotes


@click.group()
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, verbose):
    ctx.obj["VERBOSE"] = verbose


@cli.command(help='读取股票行情数据.')
@click.option('-s', '--symbol', default='600001', help='股票代码')
@click.option('-m', '--method', default='bars', help='操作方法')
@click.option('-t', '--tofile', default='feed.csv', help='输出文件')
def quotes(symbol, method, tofile):
    client = Quotes()
    feed = getattr(client, method)(symbol=symbol)

    if tofile:
        feed.to_csv(tofile)

    print(feed)


@cli.command(help='测试行情服务器.')
@click.option('-l', '--limit', default='5', help='显示最快几个')
@click.option('-t', '--tofile', default=None, help='输出文件')
@click.option('-v', '--verbose', count=True)
def verify(limit, verbose, tofile):
    check(limit=int(limit), verbose=verbose, tofile=tofile)


def execute():
    cli(obj={})
