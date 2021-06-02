# -*- coding: utf-8 -*-
import pandas as pd


def QA_data_make_qfq(bfq_data, xdxr_data):
    # '使用数据库数据进行复权'
    info = xdxr_data.query('category==1')
    bfq_data = bfq_data.assign(if_trade=1)

    if len(info) > 0:
        data = pd.concat([
            bfq_data, info.loc[bfq_data.index[0]:bfq_data.index[-1],
                               ['category']]
        ],
                         axis=1)
        data['if_trade'].fillna(value=0, inplace=True)
        data = data.fillna(method='ffill')
        data = pd.concat([
            data, info.loc[bfq_data.index[0]:bfq_data.index[-1],
                           ['fenhong', 'peigu', 'peigujia', 'songzhuangu']]
        ],
                         axis=1)
    else:
        data = pd.concat([
            bfq_data, info.
            loc[:, ['category', 'fenhong', 'peigu', 'peigujia', 'songzhuangu']]
        ],
                         axis=1)

    data = data.fillna(0)
    data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] +
                        data['peigu'] * data['peigujia']) / (
                            10 + data['peigu'] + data['songzhuangu'])
    data['adj'] = (data['preclose'].shift(-1) /
                   data['close']).fillna(1)[::-1].cumprod()
    data['open'] = data['open'] * data['adj']
    data['high'] = data['high'] * data['adj']
    data['low'] = data['low'] * data['adj']
    data['close'] = data['close'] * data['adj']
    data['preclose'] = data['preclose'] * data['adj']
    data['volume'] = data['volume'] / data[
        'adj'] if 'volume' in data.columns else data['vol'] / data['adj']

    try:
        data['high_limit'] = data['high_limit'] * data['adj']
        data['low_limit'] = data['high_limit'] * data['adj']
    except:
        pass

    return data.query('if_trade==1 and open != 0').drop([
        'fenhong', 'peigu', 'peigujia', 'songzhuangu', 'if_trade', 'category'
    ],
                                                        axis=1)


def QA_data_make_hfq(bfq_data, xdxr_data):
    # '使用数据库数据进行复权'
    info = xdxr_data.query('category==1')
    bfq_data = bfq_data.assign(if_trade=1)

    if len(info) > 0:
        data = pd.concat([
            bfq_data, info.loc[bfq_data.index[0]:bfq_data.index[-1],
                               ['category']]
        ],
                         axis=1)

        data['if_trade'].fillna(value=0, inplace=True)
        data = data.fillna(method='ffill')

        data = pd.concat([
            data, info.loc[bfq_data.index[0]:bfq_data.index[-1],
                           ['fenhong', 'peigu', 'peigujia', 'songzhuangu']]
        ],
                         axis=1)
    else:
        data = pd.concat([
            bfq_data, info.
            loc[:, ['category', 'fenhong', 'peigu', 'peigujia', 'songzhuangu']]
        ],
                         axis=1)
    data = data.fillna(0)
    data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] +
                        data['peigu'] * data['peigujia']) / (
                            10 + data['peigu'] + data['songzhuangu'])
    data['adj'] = (data['close'] /
                   data['preclose'].shift(-1)).cumprod().shift(1).fillna(1)
    data['open'] = data['open'] * data['adj']
    data['high'] = data['high'] * data['adj']
    data['low'] = data['low'] * data['adj']
    data['close'] = data['close'] * data['adj']
    data['preclose'] = data['preclose'] * data['adj']
    data['volume'] = data['volume'] / \
                     data['adj'] if 'volume' in data.columns else data['vol'] / data['adj']
    try:
        data['high_limit'] = data['high_limit'] * data['adj']
        data['low_limit'] = data['high_limit'] * data['adj']
    except:
        pass

    return data.query('if_trade==1 and open != 0').drop(
        ['fenhong', 'peigu', 'peigujia', 'songzhuangu'], axis=1)


def _QA_data_stock_to_fq(bfq_data, xdxr_data, fqtype):
    # '使用数据库数据进行复权'
    info = xdxr_data.query('category==1')
    bfq_data = bfq_data.assign(if_trade=1)

    if len(info) > 0:
        data = pd.concat([
            bfq_data, info.loc[bfq_data.index[0]:bfq_data.index[-1],
                               ['category']]
        ],
                         axis=1)

        data['if_trade'].fillna(value=0, inplace=True)
        data = data.fillna(method='ffill')
        data = pd.concat([
            data, info.loc[bfq_data.index[0]:bfq_data.index[-1],
                           ['fenhong', 'peigu', 'peigujia', 'songzhuangu']]
        ],
                         axis=1)
    else:
        data = pd.concat([
            bfq_data, info.
            loc[:, ['category', 'fenhong', 'peigu', 'peigujia', 'songzhuangu']]
        ],
                         axis=1)

    data = data.fillna(0)
    data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] +
                        data['peigu'] * data['peigujia']) / (
                            10 + data['peigu'] + data['songzhuangu'])

    if fqtype in ['01', 'qfq']:
        data['adj'] = (data['preclose'].shift(-1) /
                       data['close']).fillna(1)[::-1].cumprod()
    else:
        data['adj'] = (data['close'] /
                       data['preclose'].shift(-1)).cumprod().shift(1).fillna(1)

    for col in ['open', 'high', 'low', 'close', 'preclose']:
        data[col] = data[col] * data['adj']

    data['volume'] = data['volume'] / \
                     data['adj'] if 'volume' in data.columns else data['vol'] / data['adj']

    try:
        data['high_limit'] = data['high_limit'] * data['adj']
        data['low_limit'] = data['high_limit'] * data['adj']
    except:
        pass

    query = 'if_trade==1 and open != 0'
    prame = [
        'fenhong', 'peigu', 'peigujia', 'songzhuangu', 'if_trade', 'category'
    ]
    return data.query(query).drop(prame, axis=1, errors='ignore')


def QA_data_stock_to_fq(__data, type_='01'):
    def __QA_fetch_stock_xdxr(code,
                              format_='pd',
                              collections=DATABASE.stock_xdxr):
        # '获取股票除权信息/数据库'
        try:
            data = [item for item in collections.find({'code': code})]
            data = pd.DataFrame(data).drop(['_id'], axis=1)
            data['date'] = pd.to_datetime(data['date'])
            return data.set_index(['date', 'code'], drop=False)
        except:

            columns = [
                'category', 'category_meaning', 'code', 'date', 'fenhong',
                'fenshu', 'liquidity_after', 'liquidity_before', 'name',
                'peigu', 'peigujia', 'shares_after', 'shares_before',
                'songzhuangu', 'suogu', 'xingquanjia'
            ]

            return pd.DataFrame(data=[], columns=columns)

    # '股票 日线/分钟线 动态复权接口'
    code = __data.index.remove_unused_levels().levels[1][0] if isinstance(
        __data.index, pd.core.indexes.multi.MultiIndex) else __data['code'][0]

    return _QA_data_stock_to_fq(bfq_data=__data,
                                xdxr_data=__QA_fetch_stock_xdxr(code),
                                fqtype=type_)

    if type_ in ['01', 'qfq']:
        return QA_data_make_qfq(__data, __QA_fetch_stock_xdxr(code))
    elif type_ in ['02', 'hfq']:
        return QA_data_make_hfq(__data, __QA_fetch_stock_xdxr(code))
    else:
        QA_util_log_info('wrong fq type! Using qfq')
        return QA_data_make_qfq(__data, __QA_fetch_stock_xdxr(code))
