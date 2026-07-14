"""Corporate-action factor retrieval."""

from __future__ import annotations

import json
import re

import httpx
import pandas as pd

from mootdx.cache import file_cache
from mootdx.utils import get_config_path, get_stock_market

DEFAULT_TIMEOUT = httpx.Timeout(10.0, connect=5.0)
_FACTOR_PAYLOAD = re.compile(r"^[^=]*=(?P<payload>.+?);?\s*$", re.DOTALL)


def _parse_factor_payload(text: str, method: str) -> pd.DataFrame:
    match = _FACTOR_PAYLOAD.match(text.strip())
    if not match:
        raise ValueError(f"新浪 {method} 复权因子响应格式无效")
    payload = json.loads(match.group("payload").rstrip(";"))
    rows = payload.get("data", [])
    if not rows:
        raise ValueError(f"新浪 {method} 复权因子不可用")

    result = pd.DataFrame(rows, columns=["date", "factor"])
    result["date"] = pd.to_datetime(result["date"], errors="raise")
    result["factor"] = pd.to_numeric(result["factor"], errors="raise")
    return result.set_index("date").sort_index()


def fq_factor(symbol: str, method: str) -> pd.DataFrame:
    method = method.lower()
    if method not in {"qfq", "hfq"}:
        raise ValueError("method 必须是 'qfq' 或 'hfq'")

    raw_symbol = symbol.strip().lower()
    for prefix in ("sh", "sz", "bj"):
        if raw_symbol.startswith(prefix):
            raw_symbol = raw_symbol[len(prefix):]
            break
    market = get_stock_market(raw_symbol, string=True)
    qualified = f"{market}{raw_symbol}"
    cache_file = get_config_path(f"caches/factor/{qualified}-{method}.pkl")

    @file_cache(filepath=cache_file, refresh_time=24 * 3600)
    def _factor() -> pd.DataFrame:
        url = f"https://finance.sina.com.cn/realstock/company/{qualified}/{method}.js"
        with httpx.Client(timeout=DEFAULT_TIMEOUT, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
        return _parse_factor_payload(response.text, method)

    return _factor()
