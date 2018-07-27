from mootdx.quotes import Quotes

client = Quotes.factory(market='std', multithread=True, heartbeat=True) # 标准市场
client = Quotes.factory(market='ext', multithread=True, heartbeat=True) # 扩展市场

# client.config(multithread=True, heartbeat=True)
client.bars(symbol='600036', category=9, offset=10)
client.index(symbol='000001', category=9)
client.minute(symbol='000001')
