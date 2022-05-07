from mootdx.contrib.data_fq import stock_to_fq
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')
bfq_data = client.bars(symbol='600036')
xdxr_data = client.xdxr(symbol='600036')
bfq_data['code'] = '600036'
# result = adjust.before(bfq_data, xdxr_data)
# print(result)

# result = adjust.after(bfq_data, xdxr_data)
# print(result)
if __name__ == '__main__':
    print(bfq_data)
    result = stock_to_fq(bfq_data, xdxr_data, '01')
    print(result)
