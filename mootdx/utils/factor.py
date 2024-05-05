import httpx
import pandas as pd

from mootdx.cache import file_cache
from mootdx.logger import logger
from mootdx.utils import get_config_path
from mootdx.utils import get_stock_market


def fq_factor(symbol: str, method: str, ) -> pd.DataFrame:
    symbol = symbol.replace('sh', '').replace('sz', '').replace('bj', '')
    market = get_stock_market(symbol, string=True)
    symbol = f'{market}{symbol}'
    cache_file = get_config_path(f'caches/factor/{symbol}.plk')

    @file_cache(filepath=cache_file, refresh_time=3600 * 24)
    def _factor(symbol: str, method: str, ) -> pd.DataFrame:

        try:
            url = 'https://finance.sina.com.cn/realstock/company/{}/{}.js'
            rsp = httpx.get(url.format(symbol, method))
            res = pd.DataFrame(eval(rsp.text.split('=')[1].split('\n')[0])['data'])
        except (SyntaxError, httpx.ConnectError) as ex:
            logger.error(ex)
            return pd.DataFrame(None)

        if res.shape[0] == 0:
            raise ValueError(f'sina {method} factor not available')

        res.columns = ['date', 'factor']
        res.date = pd.to_datetime(res.date)

        res.set_index('date', inplace=True)
        return res

    return _factor(symbol, method)


if __name__ == '__main__':
    fq = fq_factor('600036', 'qfq')
    print(fq)
