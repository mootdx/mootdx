import unittest

import pytest

from mootdx.tools.tdx2csv import txt2csv


class TestTdx2csv(unittest.TestCase):

    def test_success(self):
        with pytest.raises(FileNotFoundError):
            assert txt2csv(infile='600000') is None

    def test_exception(self):
        with pytest.raises(ValueError):
            assert txt2csv(infile='setup.cfg') is None

        with pytest.raises(FileNotFoundError):
            assert txt2csv(infile='/tmp/1.txt') is None


if __name__ == '__main__':
    unittest.main()
