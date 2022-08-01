import pytest

from mootdx.utils.holiday import holiday, holiday_, holiday2


# @pytest.mark.skip
class TestHoliday:
    def test_holiday_exists(self):
        assert holiday("2022-01-23")

    def test_holiday_country(self):
        assert holiday("2022-01-23", "%Y-%m-%d", "法国")

        with pytest.raises(ValueError):
            holiday("20220126")

        with pytest.raises(ValueError):
            holiday("2022-01-26", "%Y-%m-%d", country="巴西")

    def test_holiday_not(self):
        assert not holiday("2022-01-26")

    def test_holiday_fmt(self):
        assert holiday("2022-01-23", "%Y-%m-%d")


@pytest.mark.skip
class Testholiday0:
    def test_holiday_exists(self):
        assert holiday_("2022-01-23").empty

    def test_holiday_today(self):
        assert holiday_().empty

    def test_holiday_not(self):
        assert holiday_("2022-01-26").empty

    def test_holiday_fmt(self):
        assert holiday_("2022-01-23", "%Y-%m-%d").empty

    def test_holiday_country(self):
        assert holiday_("2022-01-23", "%Y-%m-%d", "法国").empty

        with pytest.raises(ValueError):
            holiday_("20220126")

        with pytest.raises(ValueError):
            holiday_("2022-01-26", "%Y-%m-%d", country="巴西")


class Testholiday2:
    def test_holiday_exists(self):
        assert holiday2("2022-01-23")

    def test_holiday_today(self):
        assert not holiday2().empty

    def test_holiday2not(self):
        assert holiday2("2022-01-26")
