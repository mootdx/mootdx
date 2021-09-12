from mootdx.quotes import Quotes

client = Quotes.factory(market='std')  # 标准市场
# client = Quotes.factory(market='ext', multithread=True, heartbeat=True) # 扩展市场

quote = client.bars(symbol='600036', frequency=9, offset=10)
print(quote)

quote = client.index(symbol='000001', frequency=9)
print(quote)

quote = client.minute(symbol='000001')
print(quote)
