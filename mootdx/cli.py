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
import click

@click.group()
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, verbose):
    ctx.obj["VERBOSE"] = verbose

@cli.command(help='金融产品的历史数据下载.')
@click.option('--delay', default='0.5', help='默认每次请求后等待时间')
@click.option('--thread', default='0.5', help='默认每次请求后等待时间')
def fetch(delay, thread):
    pass

@cli.command(help='读取金融产品的历史数据.')
@click.option('--delay', default='0.5', help='默认每次请求后等待时间')
@click.option('--thread', default='0.5', help='默认每次请求后等待时间')
def read(delay, thread):
    pass

def main():
    cli(obj={})
