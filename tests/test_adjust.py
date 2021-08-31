import unittest

import vcr

from mootdx.contrib.adjust import get_adjust_year


class TestAdjust(unittest.TestCase):
    def setup_class(self) -> None:
        pass

    def teardown_class(self):
        pass

    def test_adjust_before0(self):
        with vcr.use_cassette("tests/fixtures/vcr_cassettes/test_adjust_before0.yaml"):
            data = get_adjust_year(symbol="600000", year="2018", factor="before")
            self.assertFalse(data.empty)

    def test_adjust_before1(self):
        with vcr.use_cassette("tests/fixtures/vcr_cassettes/test_adjust_before1.yaml"):
            data = get_adjust_year(symbol="600000", year="2018", factor="01")
            self.assertFalse(data.empty)

    def test_adjust_before2(self):
        with vcr.use_cassette("tests/fixtures/vcr_cassettes/test_adjust_before2.yaml"):
            data = get_adjust_year(symbol="600000", year="2018", factor="aa")
            self.assertTrue(data.empty)

    def test_adjust_after0(self):
        with vcr.use_cassette("tests/fixtures/vcr_cassettes/test_adjust_after0.yaml"):
            data = get_adjust_year(symbol="600000", year="2018", factor="after")
            self.assertFalse(data.empty)

    def test_adjust_after1(self):
        with vcr.use_cassette("tests/fixtures/vcr_cassettes/test_adjust_after1.yaml"):
            data = get_adjust_year(symbol="600000", year="2018", factor="02")
            self.assertFalse(data.empty)


if __name__ == "__main__":
    unittest.main()
