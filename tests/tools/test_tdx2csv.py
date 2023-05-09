from mootdx.tools.tdx2csv import txt2csv


# @pytest.mark.asyncio
# async def test_covert():
#     await covert(src="tests/fixtures/export/SH#601005.txt", dst="tests/fixtures/export/SH#601005.csv")


def test_success():
    result = txt2csv(infile="tests/fixtures/export/SH#601003.txt")
    assert not result.empty


def test_exception():
    assert txt2csv(infile="setup.cfg").empty
    assert txt2csv(infile="/tmp/1.txt").empty
