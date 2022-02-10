# @Author  : BoPo
# @Time    : 2022/5/7 13:23
# @Function:
import glob
from pathlib import Path

import pytest
from loguru import logger

from mootdx.tools.customize import Customize
from mootdx.logger import reset

reset(verbose=2)
tdxdir = 'tests/fixtures'


def setup_module():
    logger.debug('setup_module')
    blocknew = Path(tdxdir, 'T0002', 'blocknew')
    blocknew.exists() or blocknew.mkdir(parents=True)


def teardown_module():
    logger.debug('teardown_module')
    parent = Path(tdxdir, 'T0002', 'blocknew', 'blocknew.cfg').parent
    [Path(x).unlink() for x in glob.glob(f'{parent}/*.*')] and Path(parent).rmdir()


@pytest.fixture(scope='function')
def custom():
    logger.debug('custom')
    return Customize(tdxdir=tdxdir)


def test_block_create(custom):
    # 成功模式
    assert custom.create(name='龙虎榜', symbol=['600036', '600016'], blk_file='blk_file')
    assert custom.create(name='优质股', symbol=['600036', '600016'])
    assert custom.create(name=None, symbol=['600036', '600016'])
    assert custom.create(name='优质股1', symbol=['600036', '600016'])

    # 异常测试
    with pytest.raises(Exception):
        assert custom.create(name='优质股', symbol=['600036', '600016'])

    with pytest.raises(Exception):
        assert not custom.create(name='优质股2', symbol=[])

    with pytest.raises(Exception):
        assert not custom.create(name='优质股3', symbol=None)

    with pytest.raises(Exception):
        assert not custom.create(name='', symbol=None)

    with pytest.raises(Exception):
        assert not custom.create(name=None, symbol=None)


def test_block_update(custom):
    assert custom.update(name='龙虎榜', symbol=['600036'])


def test_block_search(custom):
    assert custom.search(group=True).empty is False
    assert custom.search().empty is False

    assert custom.search(name='龙虎榜')
    assert custom.search(name='龙虎榜', group=True)


def test_block_remove(custom):
    assert custom.remove(name='优质股')
    assert custom.search(name='优质股') is None
