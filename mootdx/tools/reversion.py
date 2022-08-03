import pandas as pd


def _reversion(bfq_data, xdxr_data, type_):
    """使用数据库数据进行复权"""
    info = xdxr_data.query("category==1")
    bfq_data = bfq_data.assign(if_trade=1)

    if len(info) > 0:
        # 有除权数据
        data = pd.concat([bfq_data, info.loc[bfq_data.index[0]: bfq_data.index[-1], ["category"]]], axis=1)
        data["if_trade"].fillna(value=0, inplace=True)
        data = data.fillna(method="ffill")
        data = pd.concat([data, info.loc[bfq_data.index[0]: bfq_data.index[-1], ["fenhong", "peigu", "peigujia", "songzhuangu"]]], axis=1)
    else:
        data = pd.concat([bfq_data, info.loc[:, ["category", "fenhong", "peigu", "peigujia", "songzhuangu"]]], axis=1)

    # 数据补全
    data = data.fillna(0)

    # 计算前日收盘
    data["preclose"] = (data["close"].shift(1) * 10 - data["fenhong"] + data["peigu"] * data["peigujia"]) / (10 + data["peigu"] + data["songzhuangu"])

    # 前复权
    if type_ in ["01", "qfq"]:
        data["adj"] = (data["preclose"].shift(-1) / data["close"]).fillna(1)[::-1].cumprod()

    # 后复权
    if type_ in ["02", "hfq"]:
        data["adj"] = (data["close"] / data["preclose"].shift(-1)).cumprod().shift(1).fillna(1)

    # ohlc 数据进行复权计算
    for col in ["open", "high", "low", "close", "preclose"]:
        data[col] = data[col] * data["adj"]

    data["volume"] = data.get("volume", data.get("vol"))
    data['volume'] = data['volume'] / data['adj']
    # data['volume'] = data['volume'] / data['adj'] if 'volume' in data.columns else data['vol'] / data['adj']

    try:
        # 大该是涨跌幅
        data["high_limit"] = data["high_limit"] * data["adj"]
        data["low_limit"] = data["low_limit"] * data["adj"]
    except:
        pass

    return data.query("if_trade==1 and open != 0").drop(["fenhong", "peigu", "peigujia", "songzhuangu", "if_trade", "category"], axis=1, errors="ignore")


def reversion(stock_data, xdxr, type_="01"):
    def _fetch_xdxr(symbol, collections=None):
        """获取股票除权信息/数据库"""
        columns = [
            "category",
            "category_meaning",
            "code",
            "date",
            "fenhong",
            "fenshu",
            "liquidity_after",
            "liquidity_before",
            "name",
            "peigu",
            "peigujia",
            "shares_after",
            "shares_before",
            "songzhuangu",
            "suogu",
            "xingquanjia",
        ]

        try:
            data = pd.DataFrame([item for item in collections.find({"code": symbol})]).drop(["_id"], axis=1)
            data["date"] = pd.to_datetime(data["date"], utc=False)
            return data.set_index(["date", "code"], drop=False)
        except:
            return pd.DataFrame(data=[], columns=columns)

    # '股票 日线/分钟线 动态复权接口'
    symbol = (
        stock_data.index.remove_unused_levels().levels[1][0]
        if isinstance(stock_data.index, pd.MultiIndex)
        else stock_data["code"][0]
    )
    return _reversion(bfq_data=stock_data, xdxr_data=_fetch_xdxr(symbol, xdxr), type_=type_)


# 算法一样
def baoli_qfq(df, xdxr):
    fenhong = xdxr["fenhong"]  # 分红
    peigu = xdxr["peigu"]  # 配股
    peigujia = xdxr["peigujia"]  # 配股价
    songzhuangu = xdxr["songzhuangu"]  # 送转股

    for i in range(0, len(xdxr)):
        fh = fenhong[i]
        pg = peigu[i]
        pgj = peigujia[i]
        szg = songzhuangu[i]
        date = xdxr.index[i]

        df.loc[df.index < date, "open"] = (df["open"][df.index < date] * 10 - fh + pg * pgj) / (10 + pg + szg)
        df.loc[df.index < date, "close"] = (df["close"][df.index < date] * 10 - fh + pg * pgj) / (10 + pg + szg)
        df.loc[df.index < date, "high"] = (df["high"][df.index < date] * 10 - fh + pg * pgj) / (10 + pg + szg)
        df.loc[df.index < date, "low"] = (df["low"][df.index < date] * 10 - fh + pg * pgj) / (10 + pg + szg)

    return df
