from __future__ import annotations

import pandas as pd
import pytest

from mootdx import config
from mootdx.exceptions import MootdxValidationException
from mootdx.quotes import Quotes, StdQuotes, valid_server
from mootdx.utils import to_data


class FakeHqApi:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.client = None
        self.connected = None

    def connect(self, ip, port, time_out):
        self.connected = (ip, port, time_out)
        return self

    def close(self):
        self.client = None

    def get_security_bars(self, *args):
        return [{"close": 1.0}]


def test_std_client_uses_default_when_bestip_is_empty(monkeypatch):
    monkeypatch.setattr("mootdx.quotes.TdxHq_API", FakeHqApi)
    config.setup(force=True)
    config.set("BESTIP.HQ", "")

    client = Quotes.factory("std", timeout=3)

    expected = tuple(config.get("SERVER.HQ")[0][1:3])
    assert client.server == expected
    assert client.client.connected == (*expected, 3)


@pytest.mark.parametrize("server", [(), ("127.0.0.1",), ("bad-ip", 7709), ("127.0.0.1", 0)])
def test_valid_server_rejects_invalid_values(server):
    with pytest.raises(ValueError):
        valid_server(server)


def test_factory_rejects_unknown_market():
    with pytest.raises(ValueError, match="market"):
        Quotes.factory("unknown")


class _BarsClient:
    def __init__(self):
        self.calls = []

    def get_security_bars(self, *args):
        self.calls.append(args)
        return [{"datetime": "2024-01-02 00:00", "open": 1.0}]


def test_bars_normalizes_prefixed_code_and_validates_window():
    quotes = object.__new__(StdQuotes)
    quotes.client = _BarsClient()

    result = quotes.bars("SH.600000", offset=1)

    assert not result.empty
    assert quotes.client.calls == [(9, 1, "600000", 0, 1)]
    with pytest.raises(MootdxValidationException, match="offset"):
        quotes.bars("600000", offset=0)


def test_get_k_data_returns_empty_for_empty_or_reversed_ranges():
    quotes = object.__new__(StdQuotes)
    quotes.client = _BarsClient()
    assert quotes.get_k_data("600000", "2024-01-01", "2024-01-01").empty
    assert quotes.get_k_data("600000", None, "2024-01-02").empty


def test_to_data_accepts_numpy_like_values():
    import numpy as np

    result = to_data(np.array([[1, 2], [3, 4]]))
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (2, 2)
