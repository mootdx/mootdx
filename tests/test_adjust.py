from mootdx.contrib.adjust import get_adjust_year
import unittest


class TestAdjust(unittest.TestCase):

    def test_parse_all(self):
        data = get_adjust_year(symbol='600000', year='2018', factor='before')
        self.assertFalse(data.empty)


if __name__ == '__main__':
    unittest.main()
