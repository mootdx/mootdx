from pathlib import Path

import pytest

from mootdx import get_config_path

try:
    import py_mini_racer

    mini_racer = False
except ImportError:
    mini_racer = True


class TestHoliday:
    # 初始化工作
    cache_file = get_config_path('holiday.plk')

    def test_holiday_exists(self):
        from mootdx.utils.holiday import holiday
        Path(self.cache_file).unlink(missing_ok=True)
        result = holiday("2022-01-23")
        assert result, result

    def test_holiday_country(self):
        from mootdx.utils.holiday import holiday
        assert holiday("2022-01-23", "%Y-%m-%d", "法国")

        with pytest.raises(ValueError):
            holiday("20220126")

        with pytest.raises(ValueError):
            holiday("2022-01-26", "%Y-%m-%d", country="巴西")

    def test_holiday_not(self):
        from mootdx.utils.holiday import holiday
        result = holiday("2022-01-26")
        assert result is False, result

    def test_holiday_fmt(self):
        from mootdx.utils.holiday import holiday
        assert holiday("2022-01-23", "%Y-%m-%d")
        assert holiday("20220123", "%Y%m%d")


@pytest.mark.xfail(mini_racer, reason='py_mini_racer not installed')
class TestHoliday2:
    cache_file = get_config_path('holiday2.plk')

    def test_holiday_exists(self):
        from mootdx.utils.holiday import holiday2
        Path(self.cache_file).unlink(missing_ok=True)
        assert holiday2("2022-01-23")

    def test_holiday_today(self):
        from mootdx.utils.holiday import holiday2
        assert not holiday2().empty

    def test_holiday2not(self):
        from mootdx.utils.holiday import holiday2
        assert holiday2("2022-01-26")
