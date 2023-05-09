import pytest

from mootdx.reader import Reader

tdxdir = "tests/fixtures"


@pytest.fixture(scope="function")
def reader():
    return Reader.factory(market="std", tdxdir=tdxdir)


@pytest.fixture(scope="function")
def parse():
    from mootdx.parse import BaseParse

    return BaseParse(tdxdir=tdxdir)


@pytest.mark.parametrize(
    "symbol,expected",
    [
        # ("block.dat", "T0002/hq_cache/block.dat"),
        ("block_gn.dat", "T0002/hq_cache/block_gn.dat"),
        ("block_fg.dat", "T0002/hq_cache/block_fg.dat"),
        ("block_zs.dat", "T0002/hq_cache/block_zs.dat"),
    ],
)
def test_block(reader, symbol, expected):
    result = reader.block(symbol=symbol, debug=False)
    assert not result.empty, f"result => {result}"


@pytest.mark.parametrize("symbol,expected", [("incon.dat", "incon.dat")])
def test_incon(reader, parse, symbol, expected):
    result = reader.block(symbol=symbol, debug=False)
    assert result, f"result => {result}"


@pytest.mark.parametrize("symbol,expected", [
    ("hkblock.dat", "T0002/hq_cache/hkblock.dat"),
    ("tdxhy.cfg", "T0002/hq_cache/tdxhy.cfg"),
    ("tdxzs.cfg", "T0002/hq_cache/tdxzs.cfg"),
])
def test_cfg(parse, symbol, expected):
    result = parse.cfg(expected)
    assert not result.empty
