import pytest

from mootdx.block import ParseBase
from tests.conftest import is_empty

tdxdir = '../fixtures'


# def setup_module():
#     blocknew = Path(tdxdir, 'T0002', 'blocknew')
#     blocknew.exists() or blocknew.mkdir(parents=True)
#
#
# def teardown_module():
#     parent = Path(tdxdir, 'T0002', 'blocknew', 'blocknew.cfg').parent
#     [Path(x).unlink() for x in glob.glob(f'{parent}/*.*')] and Path(parent).rmdir()
#


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


#
# @pytest.mark.parametrize('symbol,expected', [
#     ('hkblock.dat', 'T0002/hq_cache/hkblock.dat'),
# ])
# def test_cfg(reader, symbol, expected):
#     assert not reader.parse(symbol).empty
#
#
# @pytest.mark.parametrize('symbol,expected', [
#     ('incon.dat', 'incon.dat'),
# ])
# def test_incon(reader, symbol, expected):
#     assert reader.parse(symbol)

# @pytest.mark.parametrize('symbol,expected', [
#     ("tdxhy.cfg", "T0002/hq_cache/tdxhy.cfg"),
#     ("tdxzs.cfg", "T0002/hq_cache/tdxzs.cfg"),
# ])
# def test_cfg(reader, symbol, expected):
#     result = reader.parse(symbol=symbol, debug=False)
#     assert not is_empty(result), f'result => {result}'
