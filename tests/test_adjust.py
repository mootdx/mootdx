import datetime
import os
import time
import unittest
from datetime import timedelta
from pathlib import Path

import pytest

from mootdx import get_config_path
from mootdx.contrib.adjust import get_adjust_year
from mootdx.utils.adjust import get_xdxr


@pytest.mark.skip(reason='暂时不做重复测试')
class TestAdjust(unittest.TestCase):
    def test_adjust_before0(self):
        data = get_adjust_year(symbol='600000', year='2018', factor='before')
        self.assertFalse(data.empty)

    def test_adjust_before1(self):
        data = get_adjust_year(symbol='600000', year='2018', factor='01')
        self.assertFalse(data.empty)

    def test_adjust_before2(self):
        data = get_adjust_year(symbol='600000', year='2018', factor='aa')
        self.assertTrue(data.empty)

    def test_adjust_after0(self):
        data = get_adjust_year(symbol='600000', year='2018', factor='after')
        self.assertFalse(data.empty)

    def test_adjust_after1(self):
        data = get_adjust_year(symbol='600000', year='2018', factor='02')
        self.assertFalse(data.empty)


class TestAdjustUtil(unittest.TestCase):
    symbol = '600036'

    def setUp(self) -> None:
        xdxr_file = Path(get_config_path(f'xdxr/{self.symbol}.plk'))
        xdxr_file.parent.mkdir(exist_ok=True)
        xdxr_file.unlink(missing_ok=True)

    def tearDown(self) -> None:
        xdxr_file = Path(get_config_path(f'xdxr/{self.symbol}.plk'))
        xdxr_file.unlink(missing_ok=True)

    def test_get_xdxr(self):
        xdxr_file = Path(get_config_path(f'xdxr/{self.symbol}.plk'))
        self.assertFalse(xdxr_file.exists())
        get_xdxr(self.symbol)
        xdxr_time = xdxr_file.stat().st_mtime

        get_xdxr(self.symbol)
        self.assertTrue(xdxr_file.exists())
        self.assertEqual(xdxr_file.stat().st_mtime, xdxr_time)

    def test_get_xdxr_expired(self):
        expire_time = time.mktime((datetime.date.today() + timedelta(days=-1)).timetuple())
        xdxr_file = Path(get_config_path(f'xdxr/{self.symbol}.plk'))

        get_xdxr(self.symbol)

        os.utime(xdxr_file, (expire_time, expire_time))
        xdxr_time = xdxr_file.stat().st_mtime

        get_xdxr(self.symbol)

        self.assertTrue(xdxr_file.exists())
        self.assertNotEqual(xdxr_file.stat().st_mtime, xdxr_time)
