from mootdx.reader import Reader

# 初始化通达信文件读取类
reader = Reader(tdxdir='./tests/data')

# 读取分钟数据
minute = reader.minute(symbol='600036')

# 读取时间线数据
fzline = reader.fzline(symbol='600036')

# 读取日数据
daily = reader.daily(symbol='600036')

print(minute, fzline, daily)