from mootdx.quotes import Quotes
from mootdx.utils import factor

client = Quotes.factory(market='std')
bfq_data = client.k(symbol='600036')
xdxr_data = client.xdxr(symbol='600036')

result = factor.before(bfq_data, xdxr_data)
# print(result)

# result = adjust.after(bfq_data, xdxr_data)
# print(result)
