
# 行情接口API

下面是如何在程序里面调用本接口

首先需要引入

```
from mootdx.quotes import Quotes

```

然后，创建对象

```
# 标准市场
client = Quotes.factory(market='std', multithread=True, heartbeat=True) 

# 扩展市场
client = Quotes.factory(market='ext', multithread=True, heartbeat=True) 
```

之后，通常是如下的格式

```
if api.connect("119.147.212.81", 7709):
    # ... same codes...
    api.disconnect()

```

当然，我们也支持with 语法,可以省略`disconnect()`语句

```
with api.connect("119.147.212.81", 7709):
    # some codes

```

我们的数据获取届接口一般返回list结构，如果需要转化为pandas Dataframe接口，可以使用 `api.to_df` 进行转化 如：

```
data = api.get_security_bars(9, 0, "000001", 0, 10) #返回普通list
data = api.to_df(api.get_security_bars(9, 0, "000001", 0, 10)) # 返回DataFrame

```

可以使用的api方法有下列的几个。

## api方法列表

### 参数一般性约定

一般来说，股票代码和文件名称使用字符串类型，其它参数都使用数值类型

### 1 : 获取股票行情

可以获取**多**只股票的行情信息

需要传入一个列表，每个列表由一个市场代码， 一个股票代码构成的元祖构成 `[ (市场代码1， 股票代码1)，(市场代码2， 股票代码2) ... (市场代码n， 股票代码n) ]`

如：

```
api.get_security_quotes([(0, "000001"), (1, "600300")])

```

> 
注意点：非股票品种代码，有些获取的价格不是实际价格，比如可转债获取价格为实际价格*10。这是可能是TDX为了防止浮点数错误，报价在传输和存储时实际都保存为整数，然后根据品种进行处理的结果。@solensolen


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

参考 [https://github.com/rainx/mootdx/issues/5](https://github.com/rainx/mootdx/issues/5)

### 15 ：读取板块信息

参数： 板块文件名称，可以取的值限于

```
# 板块相关参数
BLOCK_SZ = "block_zs.dat"
BLOCK_FG = "block_fg.dat"
BLOCK_GN = "block_gn.dat"
BLOCK_DEFAULT = "block.dat"

```

```
api.get_and_parse_block_info("block.dat")
# 或者用我们定义好的params
api.get_and_parse_block_info(TDXParams.BLOCK_SZ)

```

## 多线程支持

由于Python的特性，一般情况下，不太建议使用多线程代码，如果需要并发访问，建议使用多进程来实现，如果要使用多线程版本，请在初始化时设置multithread参数为True

```
api = TdxHq_API(multithread=True)

```

## 心跳包

由于长时间不与服务器交互，服务器将关闭连接，所以我们实现了心跳包的机制，可以通过

```
api = TdxHq_API(heartbeat=True)

```

设置心跳包，程序会启动一个心跳包发送线程，在空闲状态下隔一段时间发送一个心跳包，注意，打开heartbeat=True选项的同时会自动打开multithread=True

## 抛出异常

我们的错误处理有两套机制，根据TdxHq_API 构造函数里的 `raise_exception` 参数来确定，如果

```
# 默认情况
api = TdxHq_API(raise_exception=False)

```

如果在调用connect 的时候，失败会返回`false`, 调用普通接口时候，如果出错的情况返回`None`

如果

```
api = TdxHq_API(raise_exception=True)

```

如果在调用connect 的时候，失败会抛出`TdxConnectionError`异常, 调用普通接口时候，如果出错的情况抛出`TdxFunctionCallError`异常

## 重连机制

在调用函数的时候，如果服务器连接断开或者其它的异常情况下，为了保证在偶发的连接断开下自动重连并重新请求数据。关于重试的周期和次数，我们通过一个自定义的类实现，你可以实现自己的重试策略

如果开启的话，需要

```
api = TdxHq_API(auto_retry=True)

```

下面是我们默认的重试策略

```
class DefaultRetryStrategy(RetryStrategy):
    """
    默认的重试策略，您可以通过写自己的重试策略替代本策略, 改策略主要实现gen方法，该方法是一个生成器，
    返回下次重试的间隔时间, 单位为秒，我们会使用 time.sleep在这里同步等待之后进行重新connect,然后再重新发起
    源请求，直到gen结束。
    """
    @classmethod
    def gen(cls):
        # 默认重试4次 ... 时间间隔如下
        for time_interval in [0.1, 0.5, 1, 2]:
            yield time_interval

```

你可以实现自己的重试机制并替换默认的，如永远重复, 间隔1秒一次（慎用）

```
class MyRetryStrategy(RetryStrategy):
    @classmethod
    def gen(cls):
      while True:
        yield 1

# 然后覆盖默认的
api.retry_strategy = MyRetryStrategy()

```

## 调试模式

如果您需要调试本代码，监控传输过程中的数据包传输情况，可以使用调试模式，使用方法是设定环境变量 TDX_DEBUG 为 1 如

```
> TDX_DEBUG=1 hqget -f 1

```

## 行情服务器列表

为了方便连接服务器，我把一些常用的服务器列表整理到到 `hosts.py` 文件中. 在程序中可以通过

```
from mootdx.config.hosts import hq_hosts

```

获取列表, 列表里的数据参考了 [https://github.com/rainx/mootdx/issues/3](https://github.com/rainx/mootdx/issues/3)

## 获取流量统计信息

```
In [12]: api.get_traffic_stats()
Out[12]:
{"first_pkg_send_time": datetime.datetime(2017, 9, 13, 13, 42, 3, 596519),
 "recv_bytes_per_second": 116.0,
 "recv_pkg_bytes": 2759,
 "recv_pkg_num": 18,
 "send_bytes_per_second": 15.0,
 "send_pkg_bytes": 368,
 "send_pkg_num": 9,
 "total_seconds": 23.716146}

```

欢迎补充并发送pr
