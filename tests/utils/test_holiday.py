from pathlib import Path
from unittest import TestCase

import pytest

from mootdx import get_config_path

try:
    import py_mini_racer

    not_mini_racer = False
except ImportError:
    not_mini_racer = True


@pytest.mark.skipif(not_mini_racer, reason='py_mini_racer not installed')
class TestHoliday(TestCase):
    # 初始化工作
    # def setUp(self) -> None:
    #     Path(get_config_path('holiday.plk')).unlink(missing_ok=True)

    def test_holiday_exists(self):
        from mootdx.utils.holiday import holiday
        result = holiday('2022-01-23')
        assert result, result

    def test_holiday_country(self):
        from mootdx.utils.holiday import holiday
        assert holiday('2022-01-23', '%Y-%m-%d', '法国')
        assert not holiday('20220126')
        assert not holiday('2022-01-26', '%Y-%m-%d', country='巴西')

    def test_holiday_not(self):
        from mootdx.utils.holiday import holiday
        result = holiday('2022-01-26')
        assert result is False, result

    def test_holiday_fmt(self):
        from mootdx.utils.holiday import holiday
        assert holiday('2022-01-23', '%Y-%m-%d')
        assert holiday('20220123', '%Y%m%d')


@pytest.mark.skipif(not_mini_racer, reason='py_mini_racer not installed')
class TestHoliday2(TestCase):
    def setUp(self) -> None:
        Path(get_config_path('caches/holidays.plk')).write_text('')

    def test_holiday_not_exists(self):
        from mootdx.utils.holiday import holiday2
        assert holiday2('2022-01-23').empty

    def test_holiday_today(self):
        from mootdx.utils.holiday import holiday2
        assert not holiday2().empty

    def test_holiday2not(self):
        from mootdx.utils.holiday import holiday2
        assert not holiday2('2022-01-26').empty


@pytest.mark.skipif(not_mini_racer, reason='py_mini_racer not installed')
def test_holidays():
    from mootdx.utils.holiday import holidays
    assert not holidays().empty
