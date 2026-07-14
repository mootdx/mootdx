from __future__ import annotations

import os
from pathlib import Path

import pytest

from mootdx.reader import Reader

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def vipdoc() -> Path:
    configured = os.environ.get("MOOTDX_TDXDIR")
    if not configured:
        pytest.skip("设置 MOOTDX_TDXDIR 后运行本地通达信数据集成测试")
    path = Path(configured)
    if not path.is_dir():
        pytest.fail(f"MOOTDX_TDXDIR 目录不存在: {path}")
    return path


@pytest.mark.parametrize("symbol,market", [("000001", "sz"), ("600000", "sh"), ("920001", "bj")])
def test_daily_from_real_vipdoc(vipdoc, symbol, market):
    reader = Reader.factory("std", tdxdir=vipdoc)
    filepath = reader.find_path(symbol, suffix="day")
    assert filepath is not None
    assert filepath.parts[-3] == market

    result = reader.daily(symbol)
    assert not result.empty
    assert result.index.is_monotonic_increasing
    assert {"open", "high", "low", "close", "amount", "volume"}.issubset(result.columns)
    assert (result[["open", "high", "low", "close"]] >= 0).all().all()


def test_accepts_install_root_and_vipdoc_path(vipdoc):
    explicit = Reader.factory("std", tdxdir=vipdoc).daily("600000")
    root = vipdoc.parent if vipdoc.name.lower() == "vipdoc" else vipdoc
    inferred = Reader.factory("std", tdxdir=root).daily("600000")
    assert explicit.equals(inferred)
