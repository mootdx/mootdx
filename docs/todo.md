## v0.9.0 (2021-01-28)

- [x] [功能] 自定义板块函数调整, 添加增、删、改、查操作
- [x] [功能] 日志等级调整为自行可配置(之前有反馈说日志等级太低, 太多无用日志，影响性能) 构造函数调整
- [x] [功能] 调整K线数据数据频次参数(frequency)的赋值方式, 原数字方式改成字符, 例如(原15分钟线值`1`改为`15m`)
- [x] [功能] 增加服务器IP功能, 构造函数里添加 `server`参数
例如：`client = Quotes.factory(market='std', server=('127.0.0.0',7727), verbose=0, quiet=True)`
- [x] [功能] 日志过滤的调整
- [x] [恢复] 恢复了holiday2
- [x] [调整] 财务数据的表头转为中文, 使用时更加直观
- [x] [修复] 复权算法, 已经修复

- [x] test_block
- [x] 修复 holiday
- [ ] 修正扩展市场离线数据读取问题
- [ ] test_incon 格式整理
- [ ] cache3 库做过期管理
- [ ] 测试代码分目录整理

# TODO

- [ ] 【基金】client.quotes查场内基金，价格大了10倍 (下载基金数据测试)
- [ ] 【可转债】离线读取通达信数据，拿到的价格为真实值的10倍 (下载可转债数据测试)
- [ ] mootdx 读取通达信本地数据复权问题 (没做)
- [ ] mootdx 请问是否可以手动指定市场服务器IP

以下，网友提供的复权代码
```python
fenhong = xdxr['fenhong']
peigu = xdxr['peigu']
peigujia = xdxr['peigujia']
songzhuangu = xdxr['songzhuangu']

for i in range(0, len(xdxr)):
    fh = fenhong[i]
    pg = peigu[i]
    pgj = peigujia[i]
    szg = songzhuangu[i]
    date = xdxr.index[i]

    df.loc[df.index < date, 'open'] = (df['open'][df.index < date] * 10 - fh + pg * pgj) / (10 + pg + szg)
    df.loc[df.index < date, 'close'] = (df['close'][df.index < date] * 10 - fh + pg * pgj) / (10 + pg + szg)
    df.loc[df.index < date, 'high'] = (df['high'][df.index < date] * 10 - fh + pg * pgj) / (10 + pg + szg)
    df.loc[df.index < date, 'low'] = (df['low'][df.index < date] * 10 - fh + pg * pgj) / (10 + pg + szg)
```
