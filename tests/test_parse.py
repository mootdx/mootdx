import pytest

from mootdx.block import ParseBase
from tests.conftest import is_empty

tdxdir = '../fixtures'


@pytest.fixture(scope='function')
def reader():
    return ParseBase(tdxdir)


@pytest.mark.parametrize('symbol,expected', [
    ("incon.dat", "incon.dat"),
    # ("block.dat", "T0002/hq_cache/block.dat"),
    ('block_gn.dat', 'T0002/hq_cache/block_gn.dat'),
    ('block_fg.dat', 'T0002/hq_cache/block_fg.dat'),
    ('block_zs.dat', 'T0002/hq_cache/block_zs.dat'),
    ("hkblock.dat", "T0002/hq_cache/hkblock.dat"),
    # ("tdxhy.cfg", "T0002/hq_cache/tdxhy.cfg"),
    ("tdxzs.cfg", "T0002/hq_cache/tdxzs.cfg"),
])
def test_block(reader, symbol, expected):
    result = reader.parse(symbol=symbol, debug=False)
    assert not is_empty(result), f'result => {symbol}'
