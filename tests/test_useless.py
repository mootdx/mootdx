import os

import pytest


@pytest.fixture(scope='function')
def remove_dep_cli():
    os.system('pip uninstall -y click prettytable')
    yield
    os.system('pip install click prettytable')


@pytest.fixture(scope='function')
def remove_dep_holiday():
    os.system('pip uninstall -y py_mini_racer')
    yield
    os.system('pip install py_mini_racer')


@pytest.mark.skip(reason="暂时不做重复测试")
def test_dep_command(recwarn, remove_dep_cli):
    with pytest.raises(SystemExit) as e:
        from mootdx.__main__ import entry
        entry()

    assert e.value.args[0] == -1, e.value.args[0]
    assert len(recwarn) >= 1

    w = recwarn.pop()
    assert w.category == DeprecationWarning


@pytest.mark.skip(reason="暂时不做重复测试")
def test_dep_holiday(recwarn, remove_dep_holiday):
    from mootdx.utils.holiday import holiday2
    holiday2("2022-01-23")

    assert len(recwarn) >= 1

    w = recwarn.pop()
    assert w.category == DeprecationWarning
