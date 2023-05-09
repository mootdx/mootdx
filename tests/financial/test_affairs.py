import glob
import unittest
from pathlib import Path

import pytest

from mootdx.affair import Affair
from mootdx.logger import logger


@pytest.mark.skip(reason="暂时不做重复测试")
class TestAffair(unittest.TestCase):
    files = []

    downdir = "tests/fixtures/tmp"

    def setup_class(self) -> None:
        logger.debug("setup_class: 获取文件列表")
        self.files = [x["filename"] for x in Affair.files()]
        Path(self.downdir).is_file() or Path(self.downdir).mkdir()

    def teardown_class(self):
        logger.debug("teardown_class: 删除测试数据")
        [Path(x).unlink() for x in glob.glob(f"{self.downdir}/*.*")]
        Path(self.downdir).rmdir()

    def test_parse_err(self):
        data = Affair.parse(downdir=self.downdir)
        self.assertIsNone(data, data)

    def test_parse_one(self):
        data = Affair.parse(downdir=self.downdir, filename=self.files[1])
        self.assertIsNotNone(data, data)

    def test_parse_export(self):
        csv_file = Path(self.downdir, self.files[1] + ".csv")
        Affair.parse(downdir=self.downdir, filename=self.files[1]).to_csv(csv_file)
        self.assertTrue(csv_file.exists())

    def test_fetch_one(self):
        Affair.fetch(downdir=self.downdir, filename=self.files[-1])
        self.assertTrue(Path(self.downdir, self.files[-1]).exists())


if __name__ == "__main__":
    unittest.main()
