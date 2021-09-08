import numpy as np
import pandas as pd

stock_header = ['open', 'close', 'high', 'low', 'vol', 'amount', 'year', 'month', 'day', 'hour', 'minute', 'datetime']
stock_code = "159901"

xdxr_data = pd.read_csv("D:/data/fhcq/" + stock_code + ".cq")
xdxr_data['fenhong'].fillna(0.00, inplace=True)
xdxr_data['suogu'].fillna(1.00, inplace=True)
xdxr_data['datetime'] = pd.to_datetime(xdxr_data[['year', 'month', 'day']])

stock_df = pd.read_csv("D:/data/" + stock_code + ".day", header=None)
stock_df.columns = stock_header

stock_df['datetime'] = pd.to_datetime(stock_df['datetime'])
stock_df.sort_values(by='datetime', ascending=True, inplace=True)
stock_df.reset_index(drop=True, inplace=True)
stock_df['qfq_close'] = stock_df['close']
# bfq_data
# def before(bfq_data, xdxr_data):

for i in range(0, xdxr_data.shape[0]):
    category = xdxr_data['category'].iloc[i]
    fenhong = xdxr_data['fenhong'].iloc[i]
    suogu = xdxr_data['suogu'].iloc[i]
    fh_time = xdxr_data['datetime'].iloc[i]

    if category == 1:
        stock_df['qfq_close'] = np.where(stock_df['datetime'] < fh_time, stock_df['qfq_close'] - fenhong / 10,
                                         stock_df['qfq_close'])
    elif category == 11:
        stock_df['qfq_close'] = np.where(stock_df['datetime'] < fh_time, stock_df['qfq_close'] / suogu,
                                         stock_df['qfq_close'])

# print(stock_df[stock_df['datetime'] == "2021-04-09 15:00:00"])
# print(stock_df[stock_df['datetime'] == "2021-04-12 15:00:00"])
# print(stock_df)
