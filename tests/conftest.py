import pandas
import pytest

from mootdx.quotes import Quotes


def is_empty(obj):
    if isinstance(obj, pandas.DataFrame):
        return obj.empty

    print(obj)
    return not obj


@pytest.fixture()
def quotes():
    return Quotes.factory('std')
