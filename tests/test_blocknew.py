import glob
from pathlib import Path

import pytest

from mootdx.reader import Reader

tdxdir = 'tests/fixtures'


def setup_module():
    blocknew = Path(tdxdir, 'T0002', 'blocknew')
    blocknew.exists() or blocknew.mkdir(parents=True)


def teardown_module():
    parent = Path(tdxdir, 'T0002', 'blocknew', 'blocknew.cfg').parent
    [Path(x).unlink() for x in glob.glob(f'{parent}/*.*')] and Path(parent).rmdir()


@pytest.fixture(scope='function')
def reader():
    return Reader.factory(market='std', tdxdir=tdxdir)


def test_blocknew_01(reader):
    result = reader.block_new(name='最优盈利板块', symbol=['600001', '600002', '600003', '600004'])
    assert result
    print(result)


def test_blocknew_02(reader):
    result = reader.block_new(name='最优盈利板块')
    assert result

    result = reader.block_new()
    assert not result.empty, result
