"""Readers for local TongDaXin data files."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import pandas as pd
from tdxpy.reader import TdxExHqDailyBarReader, TdxLCMinBarReader, TdxMinBarReader

from mootdx.contrib.compat import MooTdxDailyBarReader
from mootdx.exceptions import MootdxValidationException
from mootdx.utils import get_stock_market, to_data


class Reader:
    @staticmethod
    def factory(market: str = "std", **kwargs):
        if not isinstance(market, str):
            raise MootdxValidationException("market 必须是 'std' 或 'ext'")
        market = market.lower()
        if market == "std":
            return StdReader(**kwargs)
        if market == "ext":
            return ExtReader(**kwargs)
        raise MootdxValidationException("market 必须是 'std' 或 'ext'")


class ReaderBase:
    """Base local reader accepting either a TDX root or its ``vipdoc`` path."""

    def __init__(self, tdxdir: str | Path | None = None) -> None:
        if tdxdir is None:
            raise MootdxValidationException("tdxdir 不能为空")

        supplied = Path(tdxdir).expanduser()
        if not supplied.is_dir():
            raise NotADirectoryError(f"tdxdir 目录不存在: {supplied}")

        if supplied.name.lower() == "vipdoc":
            self.vipdoc = supplied
            self.tdxdir = supplied.parent
        else:
            self.tdxdir = supplied
            self.vipdoc = supplied / "vipdoc"

        if not self.vipdoc.is_dir():
            raise NotADirectoryError(f"vipdoc 目录不存在: {self.vipdoc}")

    def find_path(
        self,
        symbol: str,
        subdir: str = "lday",
        suffix: str | Sequence[str] | None = None,
        **kwargs,
    ) -> Path | tuple[str, str, list[str]] | None:
        if not isinstance(symbol, str) or not symbol.strip():
            raise MootdxValidationException("symbol 不能为空")

        symbol = symbol.strip().lower()
        if "#" in symbol:
            market = "ds"
        elif symbol.startswith("88"):
            market = "sh"
        else:
            market = get_stock_market(symbol, string=True)

        if market in {"sh", "sz", "bj"}:
            for prefix in ("sh", "sz", "bj"):
                if symbol.startswith(prefix):
                    symbol = symbol[len(prefix):]
                    break
            symbol = f"{market}{symbol}"

        if suffix is None:
            suffixes: list[str] = []
        elif isinstance(suffix, str):
            suffixes = [suffix]
        else:
            suffixes = list(suffix)
        suffixes = [item.lstrip(".") for item in suffixes if item]

        if kwargs.get("debug"):
            return market, symbol, suffixes

        for extension in suffixes:
            candidate = self.vipdoc / market / subdir / f"{symbol}.{extension}"
            if candidate.is_file():
                return candidate
        return None


class StdReader(ReaderBase):
    """Reader for Shanghai, Shenzhen and Beijing securities."""

    def daily(self, symbol: str, **kwargs) -> pd.DataFrame:
        normalized = Path(symbol).stem
        filepath = self.find_path(normalized, subdir="lday", suffix="day")
        result = MooTdxDailyBarReader().get_df(str(filepath)) if filepath else None
        return to_data(result, symbol=normalized, **kwargs)

    def minute(self, symbol: str, suffix: int | str = 1, **kwargs) -> pd.DataFrame:
        normalized = Path(symbol).stem
        is_five_minute = str(suffix) == "5"
        subdir = "fzline" if is_five_minute else "minline"
        extensions = ["lc5", "5"] if is_five_minute else ["lc1", "1"]
        filepath = self.find_path(normalized, subdir=subdir, suffix=extensions)
        if filepath is None:
            return pd.DataFrame()

        parser = TdxLCMinBarReader() if filepath.suffix.startswith(".lc") else TdxMinBarReader()
        return to_data(parser.get_df(str(filepath)), symbol=normalized, **kwargs)

    def fzline(self, symbol: str, **kwargs) -> pd.DataFrame:
        return self.minute(symbol, suffix=5, **kwargs)

    def block_new(self, name: str | None = None, symbol: list[str] | None = None, group: bool = False, **kwargs):
        from mootdx.tools.customize import Customize

        reader = Customize(tdxdir=str(self.tdxdir))
        if symbol:
            return reader.create(name=name, symbol=symbol, **kwargs)
        return reader.search(name=name, group=group)

    def block(self, symbol: str = "", group: bool = False, **kwargs):
        from mootdx.parse import BaseParse

        return BaseParse(str(self.tdxdir)).parse(symbol, group=group, **kwargs)


class ExtReader(ReaderBase):
    """Reader for TDX extended-market files."""

    def __init__(self, tdxdir: str | Path | None = None) -> None:
        super().__init__(tdxdir)
        self.reader = TdxExHqDailyBarReader()

    def daily(self, symbol: str) -> pd.DataFrame:
        filepath = self.find_path(symbol, subdir="lday", suffix="day")
        return to_data(self.reader.get_df(str(filepath)) if filepath else None)

    def minute(self, symbol: str) -> pd.DataFrame:
        filepath = self.find_path(symbol, subdir="minline", suffix=["lc1", "1"])
        return to_data(self.reader.get_df(str(filepath)) if filepath else None)

    def fzline(self, symbol: str) -> pd.DataFrame:
        filepath = self.find_path(symbol, subdir="fzline", suffix=["lc5", "5"])
        return to_data(self.reader.get_df(str(filepath)) if filepath else None)
