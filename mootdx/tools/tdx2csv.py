"""Convert text files exported by TDX to CSV."""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

from mootdx.logger import logger

_COLUMNS = ["date", "open", "high", "low", "close", "volume", "amount"]


def txt2csv(infile: str | Path, outfile: str | Path | None = None) -> pd.DataFrame:
    source = Path(infile)
    try:
        frame = pd.read_csv(
            source,
            names=_COLUMNS,
            header=2,
            skipfooter=1,
            index_col="date",
            engine="python",
            encoding="gbk",
        )
    except (FileNotFoundError, OSError, UnicodeError, ValueError, TypeError, pd.errors.ParserError) as exc:
        logger.warning("无法解析通达信导出文件 %s: %s", source, exc)
        return pd.DataFrame()

    destination = Path(outfile) if outfile is not None else source.with_suffix(".csv")
    destination.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(destination)
    return frame


async def convert(src: str | Path, dst: str | Path) -> pd.DataFrame:
    return await asyncio.to_thread(txt2csv, src, dst)


async def covert(src: str | Path, dst: str | Path) -> pd.DataFrame:
    """Deprecated misspelling retained for backwards compatibility."""

    return await convert(src, dst)


def batch(src: str | Path, dst: str | Path) -> list[pd.DataFrame]:
    source = Path(src)
    destination = Path(dst)
    destination.mkdir(parents=True, exist_ok=True)
    files = sorted(source.glob("*.txt"))
    with ThreadPoolExecutor(max_workers=min(8, max(1, len(files)))) as pool:
        return list(pool.map(lambda path: txt2csv(path, destination / path.with_suffix(".csv").name), files))


__all__ = ("batch", "convert", "covert", "txt2csv")
