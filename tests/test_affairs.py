# -*- coding: utf-8 -*-
import os
import unittest

from mootdx.affair import Affair


class TestAffair(unittest.TestCase):

    def test_parse_all(self):
        file = Affair.files()
        data = Affair.parse(downdir='tmp')
        self.assertTrue(data)

    def test_parse_one(self):
        data = Affair.parse(downdir='tmp', filename='gpcw19960630.zip')
        self.assertTrue(data)

    def setUp(self):
        if not os.path.isdir('tmp'):
            os.mkdir('tmp')

    def test_parse_export(self):
        Affair.parse(downdir='tmp', filename='gpcw19960630.zip').to_csv('gpcw19960630.csv')
        self.assertTrue(os.path.exists('gpcw19960630.csv'))

    def test_files(self):
        data = Affair.files()
        self.assertTrue(type(data) is list)

    # def test_fetch_all(self):
    #     data = Affair.fetch(downdir='tmp')
    #     self.assertTrue(data)

    def test_fetch_one(self):
        Affair.fetch(downdir='tmp', filename='gpcw19960630.zip')
        self.assertTrue(os.path.exists('gpcw19960630.csv'))


if __name__ == '__main__':
    unittest.main()
