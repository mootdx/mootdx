from pathlib import Path

import pytest

from mootdx import get_config_path
from mootdx.utils.holiday import holiday, holiday2


class TestHoliday:
    # 初始化工作
    cache_file = get_config_path('holiday.plk')

    def test_holiday_exists(self):
        Path(self.cache_file).unlink(missing_ok=True)
        result = holiday("2022-01-23")
        assert result, result

    def test_holiday_country(self):
        assert holiday("2022-01-23", "%Y-%m-%d", "法国")

        with pytest.raises(ValueError):
            holiday("20220126")

        with pytest.raises(ValueError):
            holiday("2022-01-26", "%Y-%m-%d", country="巴西")

    def test_holiday_not(self):
        result = holiday("2022-01-26")
        assert result is False, result

    def test_holiday_fmt(self):
        assert holiday("2022-01-23", "%Y-%m-%d")
        assert holiday("20220123", "%Y%m%d")


class TestHoliday2:
    cache_file = get_config_path('holiday2.plk')

    def test_holiday_exists(self):
        Path(self.cache_file).unlink(missing_ok=True)
        assert holiday2("2022-01-23")

    def test_holiday_today(self):
        assert not holiday2().empty

    def test_holiday2not(self):
        assert holiday2("2022-01-26")
