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
        # hfq_factor_df = hfq_factor_df.set_index('date')

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
        # qfq_factor_df = qfq_factor_df.set_index('date')

        return qfq_factor_df


def to_adjust(temp_df, symbol=None, adjust=None):
    # zh_sina_a_stock_hfq_url = "https://finance.sina.com.cn/realstock/company/{}/hfq.js"
    # zh_sina_a_stock_qfq_url = "https://finance.sina.com.cn/realstock/company/{}/qfq.js"

    temp_df['volume'] = temp_df['vol']
    temp_df['date'] = pd.to_datetime(temp_df[['year', 'month', 'day']])
    temp_df = temp_df.set_index('date')

    if adjust == "hfq":
        # res = requests.get(zh_sina_a_stock_hfq_url.format(symbol))
        # hfq_factor_df = pd.DataFrame(eval(res.text.split("=")[1].split("\n")[0])["data"])
        # hfq_factor_df.columns = ["date", "hfq_factor"]
        # hfq_factor_df.index = pd.to_datetime(hfq_factor_df.date)

        hfq_factor_df = fq_factor(symbol=symbol, method=adjust)
        del hfq_factor_df["date"]

        temp_df = pd.merge(temp_df, hfq_factor_df, left_index=True, right_index=True, how="outer")
        temp_df.fillna(method="ffill", inplace=True)
        temp_df = temp_df.astype(float)
        temp_df.dropna(inplace=True)
        temp_df.drop_duplicates(subset=["open", "high", "low", "close", "volume"], inplace=True)

        for field in ["open", "high", "low", "close"]:
            temp_df[field] = round(temp_df[field] * temp_df["hfq_factor"], 2)

        temp_df = temp_df.iloc[:, :-1]
        # temp_df = temp_df[start_date:end_date]

        temp_df.dropna(inplace=True)
        temp_df.reset_index(inplace=True)

        return temp_df

    if adjust == "qfq":
        # res = requests.get(zh_sina_a_stock_qfq_url.format(symbol))
        # qfq_factor_df = pd.DataFrame(eval(res.text.split("=")[1].split("\n")[0])["data"])
        # qfq_factor_df.columns = ["date", "qfq_factor"]
        # qfq_factor_df.index = pd.to_datetime(qfq_factor_df.date)
        qfq_factor_df = fq_factor(symbol=symbol, method=adjust)
        qfq_factor_df = qfq_factor_df.set_index('date')
        # del qfq_factor_df["date"]

        temp_df = pd.merge(temp_df, qfq_factor_df, left_index=True, right_index=True, how="outer")
        temp_df.fillna(method="ffill", inplace=True)

        # temp_df = temp_df.astype(float)

        for field in ["open", "high", "low", "close", "volume", 'qfq_factor']:
            temp_df[field] = temp_df[field].astype(float)

        temp_df.dropna(inplace=True)
        temp_df.drop_duplicates(subset=["open", "high", "low", "close", "volume"], inplace=True)

        for field in ["open", "high", "low", "close"]:
            temp_df[field] = round(temp_df[field] / temp_df["qfq_factor"], 2)

        temp_df = temp_df.iloc[:, :-1]
        temp_df.dropna(inplace=True)
        temp_df.reset_index(inplace=True)

        print(temp_df)
        return temp_df

    return temp_df
