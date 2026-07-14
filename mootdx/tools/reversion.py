"""Price adjustment helpers."""

from __future__ import annotations

import pandas as pd

from mootdx.utils.factor import fq_factor

_OHLC = ["open", "high", "low", "close"]
_ACTION_COLUMNS = ["fenhong", "peigu", "peigujia", "songzhuangu"]


def _method(value: str) -> str:
    normalized = str(value).lower()
    aliases = {"01": "qfq", "before": "qfq", "02": "hfq", "after": "hfq"}
    normalized = aliases.get(normalized, normalized)
    if normalized not in {"qfq", "hfq"}:
        raise ValueError("复权方式必须是 qfq/01/before 或 hfq/02/after")
    return normalized


def factor_reversion(symbol: str, method: str = "qfq", raw: pd.DataFrame | None = None) -> pd.DataFrame:
    """Adjust prices with a remote factor series without adding fake rows."""

    method = _method(method)
    if raw is None or raw.empty:
        return pd.DataFrame() if raw is None else raw.copy()

    factors = fq_factor(symbol, method).sort_index()
    if factors.empty:
        return raw.copy()

    data = raw.sort_index().copy()
    combined_index = factors.index.union(data.index).sort_values()
    aligned = factors["factor"].reindex(combined_index).ffill().bfill().reindex(data.index).astype(float)
    if method == "qfq" and aligned.iloc[-1] != 0:
        aligned = aligned / aligned.iloc[-1]

    for column in _OHLC:
        if column in data:
            data[column] = data[column].astype(float) * aligned
    data["factor"] = aligned
    return data


def _prepare_actions(xdxr_data: pd.DataFrame | None) -> pd.DataFrame:
    if xdxr_data is None or xdxr_data.empty:
        return pd.DataFrame()
    actions = xdxr_data.copy()
    if not isinstance(actions.index, pd.DatetimeIndex):
        if "date" in actions:
            actions.index = pd.to_datetime(actions["date"], errors="raise")
        elif {"year", "month", "day"}.issubset(actions.columns):
            actions.index = pd.to_datetime(actions[["year", "month", "day"]], errors="raise")
        else:
            raise ValueError("除权数据缺少日期")
    actions.index = pd.to_datetime(actions.index).normalize()
    return actions.sort_index()


def _reversion(bfq_data: pd.DataFrame, xdxr_data: pd.DataFrame, type_: str) -> pd.DataFrame:
    """Adjust stock prices using TDX category-1 corporate actions."""

    method = _method(type_)
    if bfq_data is None or bfq_data.empty:
        return pd.DataFrame() if bfq_data is None else bfq_data.copy()

    raw = bfq_data.sort_index().copy()
    actions = _prepare_actions(xdxr_data)
    if actions.empty or "category" not in actions:
        return raw
    actions = actions.loc[actions["category"].eq(1)].copy()
    if actions.empty:
        return raw

    if "volume" not in raw and "vol" in raw:
        raw["volume"] = raw["vol"]
    required = set(_OHLC + ["volume"])
    missing = sorted(required.difference(raw.columns))
    if missing:
        raise ValueError(f"行情数据缺少字段: {', '.join(missing)}")

    for column in _ACTION_COLUMNS:
        if column not in actions:
            actions[column] = 0.0
    events = actions[_ACTION_COLUMNS].groupby(level=0).last()

    original_index = raw.index
    data = raw.join(events, how="outer").sort_index()
    data[_OHLC + ["volume"]] = data[_OHLC + ["volume"]].ffill()
    data[_ACTION_COLUMNS] = data[_ACTION_COLUMNS].fillna(0.0)
    data["preclose"] = (
        data["close"].shift(1) * 10
        - data["fenhong"]
        + data["peigu"] * data["peigujia"]
    ) / (10 + data["peigu"] + data["songzhuangu"])
    ratio = (data["preclose"].shift(-1) / data["close"]).fillna(1.0)

    if method == "qfq":
        data["adj"] = ratio.iloc[::-1].cumprod()
        for column in _OHLC + ["preclose"]:
            data[column] = data[column] * data["adj"]
        data["volume"] = data["volume"] / data["adj"]
    else:
        data["adj"] = ratio.cumprod()
        for column in _OHLC + ["preclose"]:
            data[column] = data[column] / data["adj"]
        data["volume"] = data["volume"] * data["adj"]

    for column in ("high_limit", "low_limit"):
        if column in data:
            data[column] = data[column] * data["adj"] if method == "qfq" else data[column] / data["adj"]

    data = data.loc[data.index.isin(original_index) & data["open"].ne(0)]
    return data.drop(columns=_ACTION_COLUMNS, errors="ignore")


def etf_reversion(data: pd.DataFrame, xdxr: pd.DataFrame, adjust: str = "01") -> pd.DataFrame:
    """Adjust fund prices using TDX category-11 split factors."""

    method = _method(adjust)
    actions = _prepare_actions(xdxr)
    if data is None or data.empty or actions.empty or "category" not in actions:
        return data.copy()
    actions = actions.loc[actions["category"].eq(11)]
    if actions.empty or "suogu" not in actions:
        return data.copy()

    result = data.copy()
    if not isinstance(result.index, pd.DatetimeIndex):
        if {"year", "month", "day"}.issubset(result.columns):
            result.index = pd.to_datetime(result[["year", "month", "day"]])
        elif "datetime" in result:
            result.index = pd.to_datetime(result["datetime"])
        else:
            raise ValueError("基金行情缺少日期")

    factors = actions["suogu"].reindex(actions.index.union(result.index)).sort_index()
    factors = (factors.bfill() if method == "qfq" else factors.ffill()).reindex(result.index).fillna(1.0)
    if method == "qfq":
        factors = factors.shift(-1, fill_value=1.0)
    for column in _OHLC:
        result[column] = result[column] / factors if method == "qfq" else result[column] * factors
    return result


def reversion(symbol: str, stock_data: pd.DataFrame, xdxr: pd.DataFrame, type_: str = "01") -> pd.DataFrame:
    """Adjust an OHLCV frame using the supplied TDX corporate actions."""

    _method(type_)
    if symbol.startswith(("15", "16", "50", "51")):
        return etf_reversion(stock_data, xdxr, type_)
    return _reversion(stock_data, xdxr, type_)


def baoli_qfq(df: pd.DataFrame, xdxr: pd.DataFrame) -> pd.DataFrame:
    """Compatibility implementation of iterative forward adjustment."""

    result = df.copy()
    for _, action in _prepare_actions(xdxr).iterrows():
        before = result.index < action.name
        denominator = 10 + action.get("peigu", 0) + action.get("songzhuangu", 0)
        for column in _OHLC:
            result.loc[before, column] = (
                result.loc[before, column] * 10
                - action.get("fenhong", 0)
                + action.get("peigu", 0) * action.get("peigujia", 0)
            ) / denominator
    return result
