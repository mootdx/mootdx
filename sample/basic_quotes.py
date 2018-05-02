from mootdx.quotes import Quotes

# 初始化通达信客户端
client = Quotes(multithread=True, heartbeat=True)
bars = client.bars(symbol='600036', category=9, offset=10)
index = client.index(symbol='000001', category=9)
minute = client.minute(symbol='000001')

print(minute, index, bars)