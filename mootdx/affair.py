"""Download and parse TDX financial archives."""

from __future__ import annotations

import hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from mootdx.financial import financial
from mootdx.logger import logger
from mootdx.utils import TqdmUpTo


def _md5(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.md5()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(downdir: str | Path, filename: str) -> bool:
    with TqdmUpTo(unit="B", unit_scale=True, miniters=1, ascii=True) as progress:
        financial.Financial().fetch_only(report_hook=progress.update_to, filename=filename, downdir=downdir)
    return True


def fetch_file(downdir: str | Path, file_obj: dict):
    """Download one manifest entry unless a verified copy already exists."""

    filepath = Path(downdir) / file_obj["filename"]
    if filepath.is_file() and file_obj.get("hash") == _md5(filepath):
        logger.info("文件已存在且校验通过: %s", filepath)
        return filepath

    financial.Financial().fetch_only(
        report_hook=None,
        filename=file_obj["filename"],
        filesize=file_obj.get("filesize", 0),
        downdir=downdir,
    )
    if file_obj.get("hash") and _md5(filepath) != file_obj["hash"]:
        filepath.unlink(missing_ok=True)
        raise OSError(f"下载文件 MD5 校验失败: {filepath.name}")
    return filepath


class Affair:
    @staticmethod
    def parse(downdir: str | Path = ".", filename: str | None = None, **kwargs):
        if not filename:
            raise ValueError("filename 不能为空")

        filepath = Path(downdir) / filename
        if not filepath.is_file():
            Affair.fetch(downdir=downdir, filename=filename)
        if not filepath.is_file():
            raise FileNotFoundError(filepath)
        return financial.FinancialReader().to_data(filepath, **kwargs)

    @staticmethod
    def files() -> list[dict]:
        return financial.FinancialList().fetch_and_parse() or []

    @staticmethod
    def fetch(downdir: str | Path | None = None, filename: str | None = None):
        destination = Path(downdir or ".")
        destination.mkdir(parents=True, exist_ok=True)

        if filename:
            with TqdmUpTo(unit="B", unit_scale=True, miniters=1, ascii=True) as progress:
                financial.Financial().fetch_only(
                    report_hook=progress.update_to,
                    filename=filename,
                    downdir=destination,
                )
            return destination / filename

        manifest = Affair.files()
        workers = min(8, max(1, len(manifest)))
        with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="mootdx-finance") as pool:
            return list(pool.map(lambda item: fetch_file(destination, item), manifest))
