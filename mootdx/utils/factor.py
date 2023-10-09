import pandas as pd
import requests

from mootdx.utils import get_stock_market


def fq_factor(symbol: str, method: str, ) -> pd.DataFrame:
    symbol = symbol.replace('sh', '').replace('sz', '').replace('bj', '')
    market = get_stock_market(symbol, string=True)
    symbol = f'{market}{symbol}'

    url = "https://finance.sina.com.cn/realstock/company/{}/{}.js"
    rsp = requests.get(url.format(symbol, method))
    res = pd.DataFrame(eval(rsp.text.split("=")[1].split("\n")[0])["data"])

    if res.shape[0] == 0:
        raise ValueError(f"sina {method} factor not available")

    res.columns = ["date", "factor"]
    res.date = pd.to_datetime(res.date)
    res.set_index("date", inplace=True)

    return res
