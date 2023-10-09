import pandas as pd
import requests

from mootdx.cache import file_cache
from mootdx.utils import get_stock_market, get_config_path


def fq_factor(symbol: str, method: str, ) -> pd.DataFrame:
    symbol = symbol.replace('sh', '').replace('sz', '').replace('bj', '')
    market = get_stock_market(symbol, string=True)
    symbol = f'{market}{symbol}'
    cache_file = get_config_path(f'caches/factor/{symbol}.plk')

    @file_cache(filepath=cache_file, refresh_time=3600 * 24)
    def _factor(symbol: str, method: str, ) -> pd.DataFrame:
        url = "https://finance.sina.com.cn/realstock/company/{}/{}.js"
        rsp = requests.get(url.format(symbol, method))
        res = pd.DataFrame(eval(rsp.text.split("=")[1].split("\n")[0])["data"])

        if res.shape[0] == 0:
            raise ValueError(f"sina {method} factor not available")

        res.columns = ["date", "factor"]
        res.date = pd.to_datetime(res.date)
        res.set_index("date", inplace=True)
        print('~~~')
        return res

    return _factor(symbol, method)


if __name__ == '__main__':
    fq = fq_factor('600036', 'qfq')
    print(fq)
