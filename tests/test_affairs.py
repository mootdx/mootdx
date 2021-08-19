# -*- coding: utf-8 -*-
import os
import unittest

from mootdx.affair import Affair


class TestAffair(unittest.TestCase):
    files = []

    def setup_class(self) -> None:
        self.files = [x['filename'] for x in Affair.files()]

    def teardown_class(self):
        pass

    def test_parse_all(self):
        data = Affair.parse(downdir='tmp')
        self.assertIsNone(data)

    def test_parse_one(self):
        data = Affair.parse(downdir='tmp', filename=self.files[-1])
        self.assertIsNotNone(data)

    def test_parse_export(self):
        Affair.parse(downdir='tmp', filename=self.files[-1]).to_csv(self.files[-1] + '.csv')
        self.assertTrue(os.path.exists(self.files[-1] + '.csv'))

    def test_files(self):
        data = Affair.files()
        self.assertTrue(type(data) is list)

    def test_fetch_one(self):
        Affair.fetch(downdir='tmp', filename=self.files[-1])
        self.assertTrue(os.path.exists(self.files[-1] + '.csv'))


if __name__ == '__main__':
    unittest.main()
