from __future__ import annotations

import pandas as pd
import pytest

from mootdx.tools.reversion import factor_reversion, reversion


@pytest.fixture
def prices() -> pd.DataFrame:
    index = pd.date_range("2024-01-02", periods=5, freq="B")
    return pd.DataFrame(
        {
            "open": [10.0, 10.2, 9.2, 9.4, 9.6],
            "high": [10.5, 10.4, 9.5, 9.7, 9.8],
            "low": [9.8, 10.0, 9.0, 9.2, 9.4],
            "close": [10.2, 10.3, 9.4, 9.6, 9.7],
            "volume": [1000.0, 1100.0, 1200.0, 1300.0, 1400.0],
        },
        index=index,
    )


@pytest.fixture
def actions(prices) -> pd.DataFrame:
    return pd.DataFrame(
        {"category": [1], "fenhong": [1.0], "peigu": [0.0], "peigujia": [0.0], "songzhuangu": [0.0]},
        index=[prices.index[2]],
    )


@pytest.mark.parametrize("method", ["qfq", "01", "before", "hfq", "02", "after"])
def test_reversion_preserves_trading_index(prices, actions, method):
    result = reversion("600000", prices, actions, method)
    assert result.index.equals(prices.index)
    assert result[_OHLC].notna().all().all()


def test_qfq_and_hfq_adjust_volume_in_opposite_directions(prices, actions):
    qfq = reversion("600000", prices, actions, "qfq")
    hfq = reversion("600000", prices, actions, "hfq")
    assert qfq.iloc[0]["close"] < prices.iloc[0]["close"]
    assert qfq.iloc[0]["volume"] > prices.iloc[0]["volume"]
    assert hfq.iloc[-1]["close"] > prices.iloc[-1]["close"]
    assert hfq.iloc[-1]["volume"] < prices.iloc[-1]["volume"]


def test_factor_reversion_aligns_only_to_trading_days(prices, monkeypatch):
    factors = pd.DataFrame(
        {"factor": [0.8, 1.0]},
        index=pd.to_datetime(["2024-01-01", "2024-01-05"]),
    )
    monkeypatch.setattr("mootdx.tools.reversion.fq_factor", lambda symbol, method: factors)

    result = factor_reversion("600000", "qfq", prices)
    assert result.index.equals(prices.index)
    assert result.iloc[-1]["factor"] == pytest.approx(1.0)


_OHLC = ["open", "high", "low", "close"]
