from mootdx.utils.adjust import fq_factor


class TestFactor:

    def test_qfq_factor(self):
        result = fq_factor(symbol='sh600036', method='qfq')
        assert len(result), result

    def test_hfq_factor(self):
        result = fq_factor(symbol='sh600036', method='hfq')
        assert len(result), result
