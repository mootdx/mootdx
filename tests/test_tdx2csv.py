import unittest

import pytest

from mootdx.tools.tdx2csv import txt2csv, batch


class TestTdx2csv(unittest.TestCase):

    def test_batch(self):
        batch(src='../fixtures/export', dst='output')

    def test_success(self):
        result = txt2csv(infile='../fixtures/export/SH#601003.txt')
        assert not result.empty

    def test_exception(self):
        with pytest.raises(ValueError):
            assert txt2csv(infile='setup.cfg') is None

        with pytest.raises(FileNotFoundError):
            assert txt2csv(infile='/tmp/1.txt') is None


if __name__ == '__main__':
    unittest.main()
