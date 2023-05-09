import pytest


@pytest.mark.skip(reason='暂时不做重复测试')
def test_quotes(quotes):
    quotes.close()
    assert quotes.xdxr(symbol='600036').empty is False
