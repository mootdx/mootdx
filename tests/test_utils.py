import unittest

import mock
from numpy import empty

from mootdx.utils import get_config_path, md5sum, to_data


class TestMd5sum(unittest.TestCase):

    def test_md5sum_error(self):
        self.assertIsNone(md5sum('/ad/sd/sd'))

    def test_md5sum_success(self):
        print(md5sum('/vagrant/mootdx/setup.cfg'))


class TestToData(unittest.TestCase):

    def test_todata_list(self):
        self.assertTrue(not to_data([{'aa': 'aa'}]).empty)

    def test_todata_dict(self):
        self.assertTrue(not to_data({'abc': 123}).empty)

    def test_todata_empty(self):
        self.assertTrue(to_data(None).empty)
        self.assertTrue(to_data({}).empty)
        self.assertTrue(to_data([]).empty)
        self.assertTrue(to_data('aaa').empty)
        self.assertTrue(to_data(123).empty)


class Test_get_config_path(unittest.TestCase):

    @mock.patch('unipath.Path.mkdir')
    @mock.patch('platform.system')
    def test_platform_windows(self, platform_system, unipath_path_mkdir):
        platform_system.return_value = 'Windows'
        config = get_config_path(config='config.json')
        self.assertTrue('/mootdx/' in config)

    @mock.patch('unipath.Path.mkdir')
    @mock.patch('platform.system')
    def test_platform_linux(self, platform_system, unipath_path_mkdir):
        platform_system.return_value = 'Linux'
        config = get_config_path(config='config.json')
        self.assertTrue('/.mootdx/' in config)

    @mock.patch('unipath.Path.mkdir')
    @mock.patch('platform.system')
    def test_platform_Darwin(self, platform_system, unipath_path_mkdir):
        platform_system.return_value = 'Darwin'
        config = get_config_path(config='config.json')
        self.assertTrue('/.mootdx/' in config)


if __name__ == '__main__':
    unittest.main()
