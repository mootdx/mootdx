from mootdx.tools.tdx2csv import txt2csv


# @pytest.mark.asyncio
# async def test_covert():
#     await covert(src="tests/fixtures/export/SH#601005.txt", dst="tests/fixtures/export/SH#601005.csv")


def test_success(tmp_path):
    outfile = tmp_path / 'converted.csv'
    result = txt2csv(infile='tests/fixtures/export/SH#601003.txt', outfile=outfile)
    assert not result.empty
    assert outfile.is_file()


def test_exception():
    assert txt2csv(infile='setup.cfg').empty
    assert txt2csv(infile='/tmp/1.txt').empty
