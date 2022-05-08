from mootdx.contrib.reversion import reversion
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
    result = reversion(bfq_data, xdxr_data, '01')
    print(result)
