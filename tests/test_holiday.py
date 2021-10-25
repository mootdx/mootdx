from pathlib import Path

from mootdx import get_config_path
from mootdx.utils.holiday import holiday


class TestHoliday:
    cache_file = get_config_path('holiday.csv')

    def setup_method(self):
        Path(self.cache_file).exists() and Path(self.cache_file).unlink()

    def teardown_method(self):
        Path(self.cache_file).exists() and Path(self.cache_file).unlink()

    def test_holiday_exists(self):
        data = holiday(save=True)
        assert data.all().any(), data
        assert Path(self.cache_file).exists()

        data = holiday(save=True)
        assert data.all().any(), data

    def test_holiday_dataset(self):
        data = holiday()
        assert data.all().any(), data

    def test_holiday_now(self):
        data = holiday('now')
        assert data.all().any(), data

    def test_holiday_date(self):
        data = holiday('2021-10-25')
        assert data.all().any(), data
