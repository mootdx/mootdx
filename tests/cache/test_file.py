import datetime
import unittest
from pathlib import Path
from unittest import mock

import freezegun
import pandas as pd

from mootdx.cache import file_cache

NUM_SAMPLES = 10
DUMMY_TIME = datetime.datetime(2012, 1, 1, tzinfo=datetime.timezone.utc)

number_of_times_called = 0


def sample_function() -> pd.DataFrame:
    data = {
        'int': list(range(NUM_SAMPLES)),
        'str': [str(i) for i in range(NUM_SAMPLES)],
        'num': [float(i) for i in range(NUM_SAMPLES)],
    }

    return pd.DataFrame.from_dict(data)


class TestCacheFile(unittest.TestCase):
    def setUp(self) -> None:
        self.filepath = 'sample.pkl'
        Path(self.filepath).unlink(missing_ok=True)

    @mock.patch('pandas.DataFrame.to_pickle')
    def test_caches_if_not_exists(self, mock_file: mock.MagicMock) -> None:
        wrapped_func = file_cache(self.filepath)(sample_function)

        actual_df = wrapped_func()
        expected_df = sample_function()

        pd.testing.assert_frame_equal(actual_df, expected_df)
        mock_file.assert_called_once_with(self.filepath)

    @freezegun.freeze_time(DUMMY_TIME)
    @mock.patch('os.path.getmtime', return_value=DUMMY_TIME.timestamp())
    @mock.patch('pandas.DataFrame.to_pickle')
    def test_does_not_cache_if_not_expired(self, mock_file: mock.MagicMock, mock_getmtime: mock.MagicMock) -> None:
        refresh_time = 100

        expected_df = sample_function()
        with mock.patch('pandas.read_pickle', return_value=expected_df):
            wrapped_func = file_cache(self.filepath, refresh_time=refresh_time)(sample_function)

            actual_df = wrapped_func()

        pd.testing.assert_frame_equal(actual_df, expected_df)
        mock_file.assert_not_called()

    @freezegun.freeze_time(DUMMY_TIME, as_kwarg='frozen_time')
    @mock.patch('os.path.getmtime', return_value=DUMMY_TIME.timestamp())
    @mock.patch('pandas.DataFrame.to_pickle')
    def test_caches_if_expired(self, mock_file: mock.MagicMock, mock_getmtime: mock.MagicMock,
                               frozen_time=None) -> None:
        refresh_time = 100
        expiration_time = DUMMY_TIME + datetime.timedelta(seconds=refresh_time)

        expected_df = sample_function()

        frozen_time.move_to(expiration_time + datetime.timedelta(seconds=10))
        with mock.patch('pandas.read_pickle', return_value=expected_df):
            wrapped_func = file_cache(self.filepath, refresh_time=refresh_time)(sample_function)
            actual_df = wrapped_func()

        pd.testing.assert_frame_equal(actual_df, expected_df)
        mock_file.assert_called_once_with(self.filepath)
