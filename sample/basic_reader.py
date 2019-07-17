from mootdx.reader import Reader

# 初始化通达信文件读取类
reader = Reader.factory(market='std', tdxdir='./tests/data') # 标准市场
# reader = Reader.factory(market='ext', tdxdir='./tests/data') # 扩展市场

# 读取分钟数据
minute = reader.minute(symbol='600036')

# 读取时间线数据
fzline = reader.fzline(symbol='600036')

# 读取日数据
daily = reader.daily(symbol='600036')

print(minute, fzline, daily)
