import pytest

from mootdx.reader import Reader
from tests.conftest import is_empty


@pytest.fixture()
def reader():
    return Reader.factory(market='std', tdxdir='tests/fixtures')


@pytest.mark.parametrize('symbol,adjust,empty', [
    ('127021', '', False),
    ('000000', '', True),
    ('sh881478', '', False),
    ('881478', '', False),
    ('688001', 'qfq', False),
    ('000001', 'qfq', False),
    ('127021', 'qfq', False),
])
def test_daily(reader, symbol, adjust, empty):
    result = reader.daily(symbol=symbol, adjust=adjust)
    assert is_empty(result) is empty


@pytest.mark.parametrize('symbol', ['688001', '688001.5', '688001.loc1'])
def test_minute(reader, symbol):
    for suffix in ('1', '5'):
        result = reader.minute(symbol=symbol, suffix=suffix)
        assert not result.empty
