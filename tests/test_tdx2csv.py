import pytest

from mootdx.tools.tdx2csv import txt2csv


def test_success():
    with pytest.raises(FileNotFoundError):
        assert txt2csv(infile='600000') is None


def test_exception():
    with pytest.raises(ValueError):
        assert txt2csv(infile='setup.cfg') is None

    with pytest.raises(FileNotFoundError):
        assert txt2csv(infile='/tmp/1.txt') is None
