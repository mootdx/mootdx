import glob
from pathlib import Path

import pytest

from mootdx.reader import Reader

tdxdir = 'tests/fixtures'


def setup_module():
    ...


def teardown_module():
    ...


@pytest.fixture(scope='function')
def reader():
    return Reader.factory(market='std', tdxdir=tdxdir)


def test_block_new(reader):
    assert reader.block_new(name='龙虎榜', symbol=['600036'])
    assert reader.block_new(name='优质股', symbol=['600036'])
    assert reader.block_new(group=True).empty is False


@pytest.mark.parametrize("symbol,expected", [
    ("incon.dat", "incon.dat"),
    ("block.dat", "T0002/hq_cache/block.dat"),
    ("block_gn.dat", "T0002/hq_cache/block_gn.dat"),
    ("block_fg.dat", "T0002/hq_cache/block_fg.dat"),
    ("block_zs.dat", "T0002/hq_cache/block_zs.dat"),
    ("tdxhy.cfg", "T0002/hq_cache/tdxhy.cfg"),
    ("tdxzs.cfg", "T0002/hq_cache/tdxzs.cfg"),
    ("blocknew.cfg", "T0002/hq_cache/blocknew.cfg"),
])
def test_debug(reader, symbol, expected):
    result = reader.block(symbol=symbol, debug=True)
    assert result == f"{tdxdir}/{expected}", f"result => {result}"


@pytest.mark.parametrize("symbol,expected", [
    ("incon.dat", "incon.dat"),
    ("block.dat", "T0002/hq_cache/block.dat"),
    ("block_gn.dat", "T0002/hq_cache/block_gn.dat"),
    ("block_fg.dat", "T0002/hq_cache/block_fg.dat"),
    ("block_zs.dat", "T0002/hq_cache/block_zs.dat"),
    ("tdxhy.cfg", "T0002/hq_cache/tdxhy.cfg"),
    ("tdxzs.cfg", "T0002/hq_cache/tdxzs.cfg"),
    ("blocknew.cfg", "T0002/hq_cache/blocknew.cfg"),
])
def test_block(reader, symbol, expected):
    result = reader.block(symbol=symbol, debug=False)
    assert result is None, f"result => {result}"
