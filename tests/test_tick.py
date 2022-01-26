# import glob
# import pytest
# from pathlib import Path
#
# from mootdx.reader import Reader
#
# tdxdir = 'tests/fixtures'
#
#
# @pytest.mark.parametrize("symbol,expected", [
#     ("incon.dat", "incon.dat"),
#     ("block.dat", "T0002/hq_cache/block.dat"),
#     ("block_gn.dat", "T0002/hq_cache/block_gn.dat"),
#     ("block_fg.dat", "T0002/hq_cache/block_fg.dat"),
#     ("block_zs.dat", "T0002/hq_cache/block_zs.dat"),
#     ("tdxhy.cfg", "T0002/hq_cache/tdxhy.cfg"),
#     ("tdxzs.cfg", "T0002/hq_cache/tdxzs.cfg"),
#     ("blocknew.cfg", "T0002/hq_cache/blocknew.cfg"),
# ])
# def test_debug(reader, symbol, expected):
#     result = reader.block(symbol=symbol, debug=True)
#     assert result == f"{tdxdir}/{expected}", f"result => {result}"
#
#
# @pytest.mark.parametrize("symbol,expected", [
#     ("incon.dat", "incon.dat"),
#     ("block.dat", "T0002/hq_cache/block.dat"),
#     ("block_gn.dat", "T0002/hq_cache/block_gn.dat"),
#     ("block_fg.dat", "T0002/hq_cache/block_fg.dat"),
#     ("block_zs.dat", "T0002/hq_cache/block_zs.dat"),
#     ("tdxhy.cfg", "T0002/hq_cache/tdxhy.cfg"),
#     ("tdxzs.cfg", "T0002/hq_cache/tdxzs.cfg"),
#     ("blocknew.cfg", "T0002/hq_cache/blocknew.cfg"),
# ])
# def test_block(reader, symbol, expected):
#     result = reader.block(symbol=symbol, debug=False)
#     assert result is None, f"result => {result}"
