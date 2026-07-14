import unittest
from pathlib import Path

import pytest

from mootdx import get_config_path
from mootdx.utils.adjust import get_xdxr

pytestmark = pytest.mark.network


class XDXRTestCase(unittest.TestCase):
    symbol = '600000'

    def test_no_cache(self):
        Path(get_config_path(f'xdxr/{self.symbol}.plk')).unlink()
        xdxr = get_xdxr(symbol=self.symbol)

        assert xdxr.empty is False
        assert 'code' in xdxr.columns, xdxr.columns

    def test_cached(self):
        xdxr = get_xdxr(symbol=self.symbol)
        xdxr = get_xdxr(symbol=self.symbol)

        assert xdxr.empty is False
        assert 'code' in xdxr.columns, xdxr.columns
