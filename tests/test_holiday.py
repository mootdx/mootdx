import pytest

from mootdx.utils.holiday import holiday


@pytest.mark.skip
class TestHoliday:

    def test_holiday_exists(self):
        assert holiday('2022-01-23')

    def test_holiday_today(self):
        assert not holiday()

    def test_holiday_not(self):
        assert not holiday('2022-01-26')

    def test_holiday_fmt(self):
        assert holiday('2022-01-23', '%Y-%m-%d')

    def test_holiday_country(self):
        assert holiday('2022-01-23', '%Y-%m-%d', '法国')

        with pytest.raises(ValueError):
            holiday('20220126')

        with pytest.raises(ValueError):
            holiday('2022-01-26', '%Y-%m-%d', country='巴西')
#
