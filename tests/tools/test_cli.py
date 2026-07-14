from __future__ import annotations

from click.testing import CliRunner

from mootdx import __version__
from mootdx.__main__ import entry


def test_cli_version():
    result = CliRunner().invoke(entry, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_reader_cli_reads_fixture():
    result = CliRunner().invoke(
        entry,
        ["reader", "--tdxdir", "tests/fixtures", "--symbol", "127021", "--action", "daily"],
    )
    assert result.exit_code == 0, result.output
    assert "open" in result.output


def test_affair_requires_an_action():
    result = CliRunner().invoke(entry, ["affair"])
    assert result.exit_code == 2
    assert "--listfile" in result.output
