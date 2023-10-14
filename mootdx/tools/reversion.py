import logging

import pandas as pd

from mootdx.utils.factor import fq_factor

logger = logging.getLogger(__name__)


def factor_reversion(symbol: str, method: str = 'qfq', raw: pd.DataFrame = None) -> pd.DataFrame:
    factor = fq_factor(symbol, method)

    if not factor.empty:
        factor = factor.sort_index(ascending=True)
        raw = raw.sort_index(ascending=True)

        data = pd.concat([raw, factor.loc[raw.index[0]: raw.index[-1], ['factor']]], axis=1)
        data.factor = data.factor.fillna(method=('ffill', 'bfill')[method == 'qfq'], axis=0)
        data.factor = data.factor.fillna(1.0, axis=0)
        data.factor = data.factor.astype(float)

        for col in ['open', 'high', 'low', 'close', ]:
            data[col] = data[col] * data['factor']

        return data

    return raw


def _reversion(bfq_data, xdxr_data, type_):
    if len(xdxr_data) <= 0:
        return bfq_data

    """使用数据库数据进行复权"""
    info = xdxr_data.query('category==1')
    bfq_data = bfq_data.assign(if_trade=1)

    if len(info) > 0:
        # 有除权数据
        data = pd.concat([bfq_data, info.loc[bfq_data.index[0]: bfq_data.index[-1], ['category']]], axis=1)
        data['if_trade'].fillna(value=0, inplace=True)

        data = data.fillna(method='ffill')
        data = pd.concat(
            [data, info.loc[bfq_data.index[0]: bfq_data.index[-1], ['fenhong', 'peigu', 'peigujia', 'songzhuangu']]],
            axis=1)
    else:
        data = pd.concat([bfq_data, info.loc[:, ['category', 'fenhong', 'peigu', 'peigujia', 'songzhuangu']]], axis=1)

    # 数据补全
    data = data.fillna(0)

    # 计算前日收盘
    data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu'] * data['peigujia']) / (
        10 + data['peigu'] + data['songzhuangu'])

    # 前复权
    if type_.lower() in ['01', 'qfq']:
        data['adj'] = (data['preclose'].shift(-1) / data['close']).fillna(1)[::-1].cumprod()
        # ohlc 数据进行复权计算
        for col in ['open', 'high', 'low', 'close', 'preclose']:
            data[col] = data[col] * data['adj']

    # 后复权
    if type_.lower() in ['02', 'hfq']:
        data['adj'] = (data['preclose'].shift(-1) / data['close']).fillna(1).cumprod()
        for col in ['open', 'high', 'low', 'close', 'preclose']:
            data[col] = data[col] / data['adj']

    # data["volume"] = data.get("volume", data.get("vol"))
    data['volume'] = data['volume'] / data['adj']
    # data['volume'] = data['volume'] / data['adj'] if 'volume' in data.columns else data['vol'] / data['adj']

    try:
        # 大该是涨跌幅
        data['high_limit'] = data['high_limit'] * data['adj']
        data['low_limit'] = data['low_limit'] * data['adj']
    except:
        pass

    data = data.query('if_trade==1 and open != 0')
    data = data.drop(['fenhong', 'peigu', 'peigujia', 'songzhuangu', 'if_trade', 'category'], axis=1, errors='ignore')

    return data


def etf_reversion(data, xdxr, adjust='01'):
    if len(xdxr) <= 0:
        return data

    xdxr = xdxr.query('category==11')

    if len(xdxr) <= 0:
        return data

    data['date'] = pd.to_datetime(data[['year', 'month', 'day']], utc=False)

    data = data.set_index(['date'])
    data = pd.concat([data, xdxr.loc[data.index[0]: data.index[-1], ['suogu', 'category']]], axis=1)

    if adjust.lower() in ['01', 'qfq']:
        # 前复权向前移动一天
        # 向前传播
        data['suogu'] = data['suogu'].fillna(method='bfill')
        data['suogu'] = data['suogu'].fillna(1)
        data['suogu'] = data['suogu'].shift(-1)

        for col in ['open', 'high', 'low', 'close']:
            data[col] = data[col] / data['suogu']

    if adjust.lower() in ['02', 'hfq']:
        data['suogu'] = data['suogu'].fillna(method='ffill')
        data['suogu'] = data['suogu'].fillna(1)

        for col in ['open', 'high', 'low', 'close']:
            data[col] = data[col] * data['suogu']

    data = data.drop(['suogu', 'category'], axis=1, errors='ignore')
    data = data.set_index(['datetime'])

    return data


def reversion(symbol, stock_data, xdxr, type_='01'):
    def _fetch_xdxr(collections=None):
        """获取股票除权信息数据"""
        columns = [
            'category',
            'category_meaning',
            'date',
            'fenhong',
            'fenshu',
            'liquidity_after',
            'liquidity_before',
            'name',
            'peigu',
            'peigujia',
            'shares_after',
            'shares_before',
            'songzhuangu',
            'suogu',
            'xingquanjia',
        ]

        try:
            data = collections

            if len(data) <= 0:
                return data

            if 'date' not in data.columns:
                data['date'] = pd.to_datetime(data[['year', 'month', 'day']], utc=False)
                data = data.set_index(['date'])

            # data = data.drop(['year', 'month', 'day', ], axis=1)
            # data = pd.DataFrame([item for item in collections.find({"code": symbol})]).drop(["_id"], axis=1)
            # data = collections
            # data["date"] = pd.to_datetime(data["date"], utc=False)
            # data["date"] = pd.to_datetime(xdxr[["year", "month", "day"]], utc=False)
            # return data.set_index(["date", "code"], drop=False)
            return data
        except Exception as ex:
            logger.error(ex)
            return pd.DataFrame(data=[], columns=columns)

    # '股票 日线/分钟线 动态复权接口'
    # if isinstance(stock_data.index, pd.MultiIndex):
    #     symbol = stock_data.index.remove_unused_levels().levels[1][0]
    # else:
    #     symbol = stock_data["code"][0]
    # symbol = ''
    # symbol = (
    #     stock_data.index.remove_unused_levels().levels[1][0]
    #     if isinstance(stock_data.index, pd.MultiIndex)
    #     else stock_data["code"][0]
    # )

    if symbol[:2] in ['15', '16', '50', '51']:
        stock_data = etf_reversion(data=stock_data, xdxr=_fetch_xdxr(xdxr), adjust=type_)

    return factor_reversion(symbol=symbol, raw=stock_data, method=type_)
    # return _reversion(bfq_data=stock_data, xdxr_data=_fetch_xdxr(xdxr), type_=type_)


# 算法一样
def baoli_qfq(df, xdxr):
    peigu = xdxr['peigu']  # 配股
    fenhong = xdxr['fenhong']  # 分红
    peigujia = xdxr['peigujia']  # 配股价
    songzhuangu = xdxr['songzhuangu']  # 送转股

    for i in range(0, len(xdxr)):
        fh = fenhong[i]
        pg = peigu[i]
        pgj = peigujia[i]
        szg = songzhuangu[i]
        date = xdxr.index[i]

        df.loc[df.index < date, 'close'] = (df['close'][df.index < date] * 10 - fh + pg * pgj) / (10 + pg + szg)
        df.loc[df.index < date, 'open'] = (df['open'][df.index < date] * 10 - fh + pg * pgj) / (10 + pg + szg)
        df.loc[df.index < date, 'high'] = (df['high'][df.index < date] * 10 - fh + pg * pgj) / (10 + pg + szg)
        df.loc[df.index < date, 'low'] = (df['low'][df.index < date] * 10 - fh + pg * pgj) / (10 + pg + szg)

    return df
