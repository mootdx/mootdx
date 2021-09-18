import glob
import unittest
from pathlib import Path

from mootdx.affair import Affair
from mootdx.logger import logger


class TestAffair(unittest.TestCase):
    files = []

    downdir = 'tests/fixtures/tmp'

    def setup_class(self) -> None:
        logger.info('获取文件列表')
        Path(self.downdir).mkdir(parents=True)
        self.files = [x['filename'] for x in Affair.files()]

    def teardown_class(self):
        [Path(x).unlink() for x in glob.glob(f'{self.downdir}/*.*')]
        Path(self.downdir).rmdir()

    def test_parse_all(self):
        data = Affair.parse(downdir=self.downdir)
        assert not data

    def test_parse_one(self):
        data = Affair.parse(downdir=self.downdir, filename=self.files[-1])
        assert data

    def test_parse_export(self):
        csv_file = Path(self.downdir, self.files[1] + '.csv')
        Affair.parse(downdir=self.downdir, filename=self.files[-1]).to_csv(csv_file)
        assert csv_file.exists()

    def test_fetch_one(self):
        Affair.fetch(downdir=self.downdir, filename=self.files[-1])
        assert Path(self.downdir, self.files[-1]).exists()


if __name__ == '__main__':
    unittest.main()
