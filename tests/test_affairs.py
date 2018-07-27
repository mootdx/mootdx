# -*- coding: utf-8 -*-
import unittest,os

from mootdx.affairs import Affairs

class TestAffairs(unittest.TestCase):

    # def test_parse_all(self):
    #     data = Affairs.parse(downdir='tmp')
    #     self.assertTrue(data)

    # def test_parse_one(self):
    #     data = Affairs.parse(downdir='tmp', filename='gpcw19960630.zip')
    #     self.assertTrue(data)

    def test_parse_export(self):
        Affairs.parse(downdir='tmp', filename='gpcw19960630.zip').to_csv('gpcw19960630.csv')
        self.assertTrue(os.path.exists('gpcw19960630.csv'))

    def test_files(self):
        data = Affairs.files()
        self.assertTrue(type(data) is list)

    # def test_fetch_all(self):
    #     data = Affairs.fetch(downdir='tmp')
    #     self.assertTrue(data)

    def test_fetch_one(self):
        Affairs.fetch(downdir='tmp', filename='gpcw19960630.zip')
        self.assertTrue(os.path.exists('gpcw19960630.csv'))


if __name__ == '__main__':
    unittest.main()
