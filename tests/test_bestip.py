import unittest
from pathlib import Path

from mootdx import config


class TestBestIP(unittest.TestCase):

    def setUp(self) -> None:
        conf = Path.home() / '.mootdx' / 'config.json'
        conf.unlink()

    def test_config_setup(self):
        config.setup()


if __name__ == '__main__':
    unittest.main()
