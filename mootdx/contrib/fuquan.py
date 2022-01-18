# -*- coding: utf-8 -*-
# @Author  : BoPo
# @Time    : 2022/1/18 15:47
# @Function:

# array(['year', 'month', 'day', 'category', 'name', 'fenhong', 'peigujia',
#        'songzhuangu', 'peigu', 'suogu', 'panqianliutong', 'panhouliutong',
#        'qianzongguben', 'houzongguben', 'fenshu', 'xingquanjia'],
#       dtype=object)


# present  bonus  price  rationed
# 展示      奖金    价格    配给

# category == 1
# fenhong 分红
# peigujia 配股价
# songzhuangu 送转股
# peigu 配股
# suogu 缩股
# panqianliutong  盘前流通
# qianzongguben 前总股本
# houzongguben 后总股本
# fenshu 分属
# xingquanjia 行权价

# http://www.allparty.cn/yong-Pandas-ji-suan-qian-fu-quan-shu-ju.html
# http://www.cppblog.com/wangkang2009/archive/2015/04/25/210437.aspx

# https://raw.githubusercontent.com/yutiansut/QUANTAXIS/master/QUANTAXIS/QAData/data_fq.py
# https://www.cnblogs.com/whiteBear/p/12782161.html
# https://www.cnblogs.com/weidu/p/9831807.html


import pandas as pd

from mootdx.quotes import Quotes


def calc_fuquan_use_fenhong(df, df_fenhong):
    """获取复权后的历史数据, 用分红表来计算复权 , 前复权
    df: 日k线
    df_fenhong: 分红表
    return: df"""
    # 日期早的在前面
    # 经过测试， 前复权结果与同花顺，通达信的计算相同

    df_fenhong = df_fenhong.sort_index(by=2)

    for i in range(len(df_fenhong)):
        gu, money, date = df_fenhong.irow(i)

        if len(df.ix[:date]) < 2:
            continue

        # 比对日期
        date = agl.df_get_pre_date(df, date)

        if money > 0:
            money = money * 0.1
            df['o'].ix[:date] -= money
            df['h'].ix[:date] -= money
            df['c'].ix[:date] -= money
            df['l'].ix[:date] -= money
        if gu > 0:
            # x = cur / (1+y/10)
            gu = 1 + gu / 10
            df['o'].ix[:date] /= gu
            df['h'].ix[:date] /= gu
            df['c'].ix[:date] /= gu
            df['l'].ix[:date] /= gu

    return df


def make_fq(symbol='', method='00'):
    client = Quotes.factory(market='std')
    data = client.bars(symbol=symbol)
    xdxr = client.xdxr(symbol=symbol).query('category==1')

    if method:
        return make_qfq(data, xdxr, method)

    return data


# present  bonus  price  rationed
# 展示      奖金    价格    配给

def make_qfq(data, xdxr, fq_type='01'):
    """使用数据库数据进行复权"""

    # 过滤其他，只留除权信息
    xdxr = xdxr.query('category==1')
    # data = data.assign(if_trade=1)

    if len(xdxr) > 0:
        # 有除权信息, 合并原数据 + 除权数据
        # data = pd.concat([data, xdxr.loc[data.index[0]:data.index[-1], ['category']]], axis=1)
        # data['if_trade'].fillna(value=0, inplace=True)

        data = data.fillna(method='ffill')
        # present       bonus       price       rationed
        # songzhuangu   fenhong     peigujia    peigu
        data = pd.concat([data, xdxr.loc[data.index[0]:data.index[-1], ['fenhong', 'peigu', 'peigujia', 'songzhuangu']]], axis=1)
    else:
        # 没有除权信息
        data = pd.concat([data, xdxr.loc[:, ['fenhong', 'peigu', 'peigujia', 'songzhuangu']]], axis=1)

    # 清理数据
    data = data.fillna(0)

    if fq_type == '01':
        # 生成 preclose todo 关键位置

        # for key,val in ea.iterrows():
        #     date = key - datetime.timedelta(days=1)
        #     for field in df.columns.values:
        #         if field != 'volume' and field != 'amount':
        #             df.iloc[date:, field] -= val.bonus/10
        #             df.iloc[date:, field] += val.price*(val.rationed/10)
        #             df.iloc[date:, field] /= 1 + val.present/10 + val.rationed/10

        # -= val.bonus / 10 == @todo
        df1 = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu'] * data['peigujia'])
        df2 = (10 + data['peigu'] + data['songzhuangu'])

        data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu'] * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
        # 生成 adj 复权因子
        data['adj'] = (data['preclose'].shift(-1) / data['close']).fillna(1)[::-1].cumprod()
    else:
        # 生成 preclose todo 关键位置
        data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu'] * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
        # 生成 adj 复权因子
        data['adj'] = (data['close'] / data['preclose'].shift(-1)).cumprod().shift(1).fillna(1)

    # 计算复权价格
    for field in data.columns.values:
        if field in ('open', 'close', 'high', 'low', 'preclose'):
            data[field] = data[field] * data['adj']

    # 清理数据, 返回结果
    return data.query('open != 0').drop(['fenhong', 'peigu', 'peigujia', 'songzhuangu', ], axis=1)

# def make_hfq(bfq_data, xdxr_data):
#     """使用数据库数据进行复权"""
#     info = xdxr_data.query('category==1')
#     bfq_data = bfq_data.assign(if_trade=1)
#
#     if len(info) > 0:
#         # 合并数据
#         data = pd.concat([bfq_data, info.loc[bfq_data.index[0]:bfq_data.index[-1], ['category']]], axis=1)
#         data['if_trade'].fillna(value=0, inplace=True)
#
#         data = data.fillna(method='ffill')
#         data = pd.concat([data, info.loc[bfq_data.index[0]:bfq_data.index[-1], ['fenhong', 'peigu', 'peigujia', 'songzhuangu']]], axis=1)
#     else:
#         data = pd.concat([bfq_data, info.loc[:, ['category', 'fenhong', 'peigu', 'peigujia', 'songzhuangu']]], axis=1)
#
#     data = data.fillna(0)
#
#     # 生成 preclose todo 关键位置
#     data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu'] * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
#     data['adj'] = (data['close'] / data['preclose'].shift(-1)).cumprod().shift(1).fillna(1)
#
#     # 计算复权价格
#     for field in data.columns.values:
#         if field in ('open', 'close', 'high', 'low', 'preclose'):
#             data[field] = data[field] * data['adj']
#
#     # data['open'] = data['open'] * data['adj']
#     # data['high'] = data['high'] * data['adj']
#     # data['low'] = data['low'] * data['adj']
#     # data['close'] = data['close'] * data['adj']
#     # data['preclose'] = data['preclose'] * data['adj']
#
#     # 不计算 交易量
#     # data['volume'] = data['volume'] / data['adj'] if 'volume' in data.columns else data['vol'] / data['adj']
#
#     try:
#         data['high_limit'] = data['high_limit'] * data['adj']
#         data['low_limit'] = data['high_limit'] * data['adj']
#     except:
#         pass
#
#     return data.query('if_trade==1 and open != 0').drop(['fenhong', 'peigu', 'peigujia', 'songzhuangu', 'if_trade', 'category'], axis=1)
