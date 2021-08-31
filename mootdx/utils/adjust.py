import pandas as pd

from ..logger import log


def before(bfq_data, xdxr_data):
    """
    使用数据库数据进行复权

    :param bfq_data:
    :param xdxr_data:
    :return:
    """

    info = xdxr_data.query("category==1")
    bfq_data = bfq_data.assign(if_trade=1)

    if len(info) > 0:
        data = pd.concat(
            [bfq_data, info.loc[bfq_data.index[0] : bfq_data.index[-1], ["category"]]],
            axis=1,
        )
        data["if_trade"].fillna(value=0, inplace=True)
        # 分红， 配股，配给价，送转取
        columns = ["fenhong", "peigu", "peigujia", "songzhuangu"]
        data = data.fillna(method="ffill")
        data = pd.concat(
            [data, info.loc[bfq_data.index[0] : bfq_data.index[-1], columns]], axis=1
        )
    else:
        columns = ["category", "fenhong", "peigu", "peigujia", "songzhuangu"]
        data = pd.concat([bfq_data, info.loc[:, columns]], axis=1)

    data = data.fillna(0)
    data["preclose"] = (
        data["close"].shift(1) * 10 - data["fenhong"] + data["peigu"] * data["peigujia"]
    ) / (10 + data["peigu"] + data["songzhuangu"])
    data["adj"] = (data["preclose"].shift(-1) / data["close"]).fillna(1)[::-1].cumprod()

    data["open"] = data["open"] * data["adj"]
    data["high"] = data["high"] * data["adj"]
    data["low"] = data["low"] * data["adj"]
    data["close"] = data["close"] * data["adj"]
    data["preclose"] = data["preclose"] * data["adj"]
    data["volume"] = (
        data["volume"] / data["adj"]
        if "volume" in data.columns
        else data["vol"] / data["adj"]
    )

    try:
        data["high_limit"] = data["high_limit"] * data["adj"]
        data["low_limit"] = data["high_limit"] * data["adj"]
    except Exception as ex:
        log.debug(ex)

    columns = ["fenhong", "peigu", "peigujia", "songzhuangu", "if_trade", "category"]
    return data.query("if_trade==1 and open != 0").drop(columns, axis=1)


def after(bfq_data, xdxr_data):
    """
    使用数据库数据进行复权

    :param bfq_data:
    :param xdxr_data:
    :return:
    """

    info = xdxr_data.query("category==1")
    bfq_data = bfq_data.assign(if_trade=1)

    if len(info) > 0:
        data = pd.concat(
            [bfq_data, info.loc[bfq_data.index[0] : bfq_data.index[-1], ["category"]]],
            axis=1,
        )

        # 过滤空内容
        data["if_trade"].fillna(value=0, inplace=True)
        data = data.fillna(method="ffill")
        data = pd.concat(
            [
                data,
                info.loc[
                    bfq_data.index[0] : bfq_data.index[-1],
                    ["fenhong", "peigu", "peigujia", "songzhuangu"],
                ],
            ],
            axis=1,
        )
    else:
        data = pd.concat(
            [
                bfq_data,
                info.loc[
                    :, ["category", "fenhong", "peigu", "peigujia", "songzhuangu"]
                ],
            ],
            axis=1,
        )

    data = data.fillna(0)
    data["preclose"] = (
        data["close"].shift(1) * 10 - data["fenhong"] + data["peigu"] * data["peigujia"]
    ) / (10 + data["peigu"] + data["songzhuangu"])
    data["adj"] = (
        (data["close"] / data["preclose"].shift(-1)).cumprod().shift(1).fillna(1)
    )
    data["open"] = data["open"] * data["adj"]
    data["high"] = data["high"] * data["adj"]
    data["low"] = data["low"] * data["adj"]
    data["close"] = data["close"] * data["adj"]
    data["preclose"] = data["preclose"] * data["adj"]
    data["volume"] = (
        data["volume"] / data["adj"]
        if "volume" in data.columns
        else data["vol"] / data["adj"]
    )

    try:
        data["high_limit"] = data["high_limit"] * data["adj"]
        data["low_limit"] = data["high_limit"] * data["adj"]
    except Exception as ex:
        log.debug(ex)

    return data.query("if_trade==1 and open != 0").drop(
        ["fenhong", "peigu", "peigujia", "songzhuangu"], axis=1
    )
