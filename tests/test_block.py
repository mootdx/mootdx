import glob
from pathlib import Path

import pytest

import mootdx.block
from mootdx.reader import Reader

tdxdir = '../fixtures'


def setup_module():
    blocknew = Path(tdxdir, 'T0002', 'blocknew')
    blocknew.exists() or blocknew.mkdir(parents=True)


def teardown_module():
    parent = Path(tdxdir, 'T0002', 'blocknew', 'blocknew.cfg').parent
    [Path(x).unlink() for x in glob.glob(f'{parent}/*.*')] and Path(parent).rmdir()


@pytest.fixture(scope='function')
def reader():
    return Reader.factory(market='std', tdxdir=tdxdir)


def test_blocknew(reader):
    assert mootdx.block.blocknew(name='龙虎榜', symbol=['600036'], blk_file='600036')
    assert mootdx.block.blocknew(name='优质股', symbol=['600036'], blk_file='600036s')
    assert mootdx.block.blocknew(group=True).empty is False

    df = mootdx.block.blocknew()
    assert (df[df.blockname == "优质股"].code == "600036").all()


@pytest.mark.skip
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
    print(f"{tdxdir}/{expected}")
    assert result == f"{tdxdir}/{expected}", f"result => {result}"


@pytest.mark.skip
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
    assert result, f"result => {result}"
