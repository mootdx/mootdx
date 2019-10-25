
### 1 : 获取股票行情

可以获取**多**只股票的行情信息

需要传入一个列表，每个列表由一个市场代码， 一个股票代码构成的元祖构成 `[ (市场代码1， 股票代码1)，(市场代码2， 股票代码2) ... (市场代码n， 股票代码n) ]`

如：

```
api.get_security_quotes([(0, "000001"), (1, "600300")])

```

> 
注意点：非股票品种代码，有些获取的价格不是实际价格，比如可转债获取价格为实际价格x10。这是可能是TDX为了防止浮点数错误，报价在传输和存储时实际都保存为整数，然后根据品种进行处理的结果。@solensolen


### 2 : 获取k线

```python
- category-> K线种类
0 5分钟K线 1 15分钟K线 2 30分钟K线 3 1小时K线 4 日K线
5 周K线
6 月K线
7 1分钟
8 1分钟K线 9 日K线
10 季K线
11 年K线

- market -> 市场代码 0:深圳，1:上海

- stockcode -> 证券代码;

- start -> 指定的范围开始位置;

- offset -> 用户要请求的 K 线数目，最大值为 800

```

如：

```
# api.get_security_bars(9,0, "000001", 4, 3)
from mootdx.consts import KLINE_RI_K
client.bars(symbol='600000', category=KLINE_RI_K, offset=10)

client.quotes(symbol='600000')


```

### 3 : 获取市场股票数量

0 - 深圳， 1 - 上海

```
api.get_security_count(0)

```

### 4 : 获取股票列表

参数：市场代码, 起始位置 如： 0,0 或 1,100

```
api.get_security_list(1, 0)

```

### 5 : 获取指数k线

- category-> K线种类
0 5分钟K线 1 15分钟K线 2 30分钟K线 3 1小时K线 4 日K线
5 周K线
6 月K线
7 1分钟
8 1分钟K线 9 日K线
10 季K线
11 年K线
- market -> 市场代码 0:深圳，1:上海

- stockcode -> 证券代码;

- start -> 指定的范围开始位置;

- count -> 用户要请求的 K 线数目，最大值为 800


如：

```
api.get_index_bars(9,1, "000001", 1, 2)

```

### 6 : 查询分时行情

参数：市场代码， 股票代码， 如： 0,000001 或 1,600300

```
api.get_minute_time_data(1, "600300")

```

### 7 : 查询历史分时行情

参数：市场代码， 股票代码，时间 如： 0,000001,20161209 或 1,600300,20161209

```
api.get_history_minute_time_data(TDXParams.MARKET_SH, "600300", 20161209)

```

注意，在引入 TDXParams 之后， （`from mootdx.params import TDXParams`） 我们可以使用 TDXParams.MARKET_SH , TDXParams.MARKET_SZ 常量来代替 1 和 0 作为参数

### 8 : 查询分笔成交

参数：市场代码， 股票代码，起始位置， 数量 如： 0,000001,0,10

```
api.get_transaction_data(TDXParams.MARKET_SZ, "000001", 0, 30)

```

### 9 : 查询历史分笔成交

参数：市场代码， 股票代码，起始位置，日期 数量 如： 0,000001,0,10,20170209

```
api.get_history_transaction_data(TDXParams.MARKET_SZ, "000001", 0, 10, 20170209)

```

### 10 : 查询公司信息目录

参数：市场代码， 股票代码， 如： 0,000001 或 1,600300

```
api.get_company_info_category(TDXParams.MARKET_SZ, "000001")

```

### 11 : 读取公司信息详情

参数：市场代码， 股票代码, 文件名, 起始位置， 数量, 如：0,000001,000001.txt,2054363,9221

```
api.get_company_info_content(0, "000001", "000001.txt", 0, 100)

```

注意这里的 起始位置， 数量 参考上面接口的返回结果。

### 12 : 读取除权除息信息

参数：市场代码， 股票代码， 如： 0,000001 或 1,600300

```
api.get_xdxr_info(1, "600300")

```

### 13 : 读取财务信息

参数：市场代码， 股票代码， 如： 0,000001 或 1,600300

```
api.get_finance_info(0, "000001")

```

### 14 : 读取k线信息

参数：市场代码， 开始时间， 结束时间

```
get_k_data("000001","2017-07-03","2017-07-10")

```
