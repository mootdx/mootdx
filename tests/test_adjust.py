import unittest

from mootdx.contrib.adjust import get_adjust_year


class TestAdjust(unittest.TestCase):

    def test_adjust_before(self):
        data = get_adjust_year(symbol='600000', year='2018', factor='before')
        self.assertFalse(data.empty)

        data = get_adjust_year(symbol='600000', year='2018', factor='01')
        self.assertFalse(data.empty)

        data = get_adjust_year(symbol='600000', year='2018', factor='aa')
        self.assertTrue(data.empty)

    def test_adjust_after(self):
        data = get_adjust_year(symbol='600000', year='2018', factor='after')
        self.assertFalse(data.empty)

        data = get_adjust_year(symbol='600000', year='2018', factor='02')
        self.assertFalse(data.empty)


if __name__ == '__main__':
    unittest.main()
