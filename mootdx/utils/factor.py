# -*- coding: utf-8 -*-
# @Author  : BoPo
# @Time    : 2021/10/11 17:28
# @Function:
import json

import httpx
import pandas as pd
from tenacity import stop_after_attempt, wait_fixed, retry


@retry(wait=wait_fixed(2), stop=stop_after_attempt(5))
def fq_factor(method: str, symbol: str) -> pd.DataFrame:
    zh_sina_a_stock_hfq_url = "https://finance.sina.com.cn/realstock/company/{}/hfq.js"
    zh_sina_a_stock_qfq_url = "https://finance.sina.com.cn/realstock/company/{}/qfq.js"

    client = httpx.Client(verify=False)

    if method == "hfq":
        res = client.get(zh_sina_a_stock_hfq_url.format(symbol))
        hfq_factor_df = pd.DataFrame(json.loads(res.text.split("=")[1].split("\n")[0])["data"])

        if hfq_factor_df.shape[0] == 0:
            raise ValueError("sina hfq factor not available")

        hfq_factor_df.columns = ["date", "hfq_factor"]
        hfq_factor_df.index = pd.to_datetime(hfq_factor_df.date)

        del hfq_factor_df["date"]

        hfq_factor_df.reset_index(inplace=True)

        return hfq_factor_df
    else:
        res = client.get(zh_sina_a_stock_qfq_url.format(symbol))
        qfq_factor_df = pd.DataFrame(json.loads(res.text.split("=")[1].split("\n")[0])["data"])

        if qfq_factor_df.shape[0] == 0:
            raise ValueError("sina hfq factor not available")

        qfq_factor_df.columns = ["date", "qfq_factor"]
        qfq_factor_df.index = pd.to_datetime(qfq_factor_df.date)

        del qfq_factor_df["date"]

        qfq_factor_df.reset_index(inplace=True)
        return qfq_factor_df
