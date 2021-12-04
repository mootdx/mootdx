from mootdx.quotes import Quotes

client = Quotes.factory(market='std', quiet=True)  # 标准市场
# client = Quotes.factory(market='ext', multithread=True, heartbeat=True) # 扩展市场

# quote = client.bars(symbol='600036', frequency=9, offset=10)
# print(quote)
#
# quote = client.index(symbol='000001', frequency=9)
# print(quote)
#
# quote = client.minute(symbol='000001')
# print(quote)

# client = Quotes.factory(market='std')
from mootdx.logger import logger, log

logger.remove()

logger.info('------------')
log.info('-========')

rd = client.minutes('159995', '20200130')  # 这条记录不存在为啥会报异常？返回None就好了吧

print(rd)
