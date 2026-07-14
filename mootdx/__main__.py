"""Command-line interface for mootdx."""

from __future__ import annotations

import logging
from pathlib import Path

import click
from prettytable import PrettyTable

from mootdx import __version__
from mootdx.logger import logger
from mootdx.utils import get_config_path, to_file


def _enable_logging(verbose: int = 0) -> None:
    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)


def _output(frame, filename: str | None) -> None:
    if filename:
        to_file(frame, filename)
        click.echo(f"已写入 {Path(filename).resolve()}")
    else:
        click.echo(frame)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, "-V", "--version", prog_name="mootdx")
def entry() -> None:
    """读取通达信本地、在线行情及财务数据。"""


@entry.command(help="读取股票在线行情数据。")
@click.option("-o", "--output", type=click.Path(dir_okay=False, path_type=Path))
@click.option("-s", "--symbol", default="600000", show_default=True)
@click.option("-a", "--action", type=click.Choice(["daily", "minute", "fzline"]), default="daily", show_default=True)
@click.option("-m", "--market", type=click.Choice(["std", "ext"]), default="std", show_default=True)
def quotes(symbol: str, action: str, market: str, output: Path | None) -> None:
    from mootdx.quotes import Quotes

    frequency = {"daily": 9, "minute": 8, "fzline": 0}[action]
    with Quotes.factory(market=market) as client:
        frame = client.bars(symbol=symbol, frequency=frequency)
    _output(frame, str(output) if output else None)


@entry.command(help="读取股票本地行情数据。")
@click.option(
    "-d",
    "--tdxdir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    required=True,
    help="通达信安装根目录或 vipdoc 目录。",
)
@click.option("-s", "--symbol", default="600000", show_default=True)
@click.option("-a", "--action", type=click.Choice(["daily", "minute", "fzline"]), default="daily", show_default=True)
@click.option("-m", "--market", type=click.Choice(["std", "ext"]), default="std", show_default=True)
@click.option("-o", "--output", type=click.Path(dir_okay=False, path_type=Path))
def reader(symbol: str, action: str, market: str, tdxdir: Path, output: Path | None) -> None:
    from mootdx.reader import Reader

    client = Reader.factory(market=market, tdxdir=tdxdir)
    frame = getattr(client, action)(symbol=symbol)
    _output(frame, str(output) if output else None)


@entry.command(help="测试行情服务器。", name="bestip")
@click.option("-l", "--limit", type=click.IntRange(min=1), default=5, show_default=True)
@click.option("-v", "--verbose", count=True)
def bestip_command(limit: int, verbose: int) -> None:
    from mootdx.server import bestip

    _enable_logging(verbose)
    bestip(limit=limit, console=True, sync=False)
    click.echo(f"最优服务器已写入 {get_config_path('config.json')}")


@entry.command(help="下载或解析财务文件。")
@click.option("-p", "--parse", "parse_name")
@click.option("-f", "--fetch", "fetch_name")
@click.option("-a", "--downall", is_flag=True)
@click.option("-o", "--output", type=click.Path(dir_okay=False, path_type=Path))
@click.option("-d", "--downdir", type=click.Path(file_okay=False, path_type=Path), default=Path("output"))
@click.option("-l", "--listfile", is_flag=True)
@click.option("-v", "--verbose", count=True)
def affair(
    parse_name: str | None,
    fetch_name: str | None,
    downdir: Path,
    output: Path | None,
    downall: bool,
    verbose: int,
    listfile: bool,
) -> None:
    from mootdx.affair import Affair

    if verbose:
        _enable_logging(verbose)
    if listfile:
        table = PrettyTable(["filename", "filesize", "hash"])
        for item in Affair.files():
            table.add_row([item["filename"], item["filesize"], item["hash"]])
        click.echo(table)
        return

    if downall or fetch_name == "all":
        paths = Affair.fetch(downdir=downdir)
        click.echo(f"下载完成，共 {len(paths)} 个文件")
        return

    if fetch_name:
        filename = f"{Path(fetch_name).stem}.zip"
        click.echo(Affair.fetch(downdir=downdir, filename=filename))
        return

    if parse_name:
        filename = f"{Path(parse_name).stem}.zip"
        frame = Affair.parse(downdir=downdir, filename=filename)
        _output(frame, str(output) if output else None)
        return

    raise click.UsageError("请指定 --listfile、--fetch、--parse 或 --downall")


@entry.command(help="批量下载在线行情数据。")
@click.option("-o", "--output", type=click.Path(file_okay=False, path_type=Path), default=Path("bundle"))
@click.option("-s", "--symbol", default="600000", help="多个代码用逗号分隔。")
@click.option("-a", "--action", type=click.Choice(["daily", "minute", "fzline"]), default="daily")
@click.option("-m", "--market", type=click.Choice(["std", "ext"]), default="std")
@click.option("-e", "--extension", type=click.Choice(["csv", "xlsx", "json", "h5"]), default="csv")
def bundle(symbol: str, action: str, market: str, output: Path, extension: str) -> None:
    from mootdx.quotes import Quotes

    output.mkdir(parents=True, exist_ok=True)
    frequency = {"daily": 9, "minute": 8, "fzline": 0}[action]
    symbols = [code.strip() for code in symbol.replace("，", ",").split(",") if code.strip()]
    with Quotes.factory(market=market) as client:
        for code in symbols:
            frame = client.bars(symbol=code, frequency=frequency)
            to_file(frame, output / f"{code}.{extension}")
            click.echo(f"下载完成 {code}")
    click.echo(f"文件目录: {output.resolve()}")


if __name__ == "__main__":
    entry()
