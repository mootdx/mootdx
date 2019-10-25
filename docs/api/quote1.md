
# 行情接口说明

下面是如何在程序里面调用本接口

首先需要引入

```python
from mootdx.quotes import Quotes

```

然后，创建对象

```python
client = Quotes.factory(market='std', multithread=True, heartbeat=True) 
```

- 参数一般性约定

一般来说，股票代码和文件名称使用字符串类型，其它参数都使用数值类型

## 01. 查询实时行情

可以获取**多**只股票的行情信息

需要传入一个列表，每个列表由一个市场代码， 一个股票代码构成的元祖构成 `[ (市场代码1， 股票代码1)，(市场代码2， 股票代码2) ... (市场代码n， 股票代码n) ]`

如：

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std') 
client.quotes(["000001", "600300"])
```
> 注意点：非股票品种代码，有些获取的价格不是实际价格，比如可转债获取价格为实际价格*10。
> 这是可能是TDX为了防止浮点数错误，报价在传输和存储时实际都保存为整数，然后根据品种进行处理的结果。

## 02. 获取k线数据

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

- count -> 用户要请求的 K 线数目，最大值为 800

```

如：

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std') 
client.bars(9, "000001", 4, 3)
```

## 03. 查询股票数量

sz - 深圳， sh - 上海

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std') 
client.stocks(market='sh')
```

## 04. 查询股票列表

参数：市场代码, 起始位置 如： 0,0 或 1,100

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std') 
client.stock_list(market='sh')
```

## 05. 指数K线行情

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

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std') 
client.index(9, "000001", 1, 2)
```

## 06. 查询分时行情

参数：市场代码， 股票代码， 如： 0,000001 或 1,600300

```
from mootdx.quotes import Quotes

client = Quotes.factory(market='std') 
client.minute("000001")
```

## 07. 历史分时行情

参数：市场代码， 股票代码，时间 如： 0,000001,20161209 或 1,600300,20161209

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std') 
client.minute(symbol="000001", date='20161209')
```

注意，在引入 TDXParams 之后， （`from mootdx.params import TDXParams`） 我们可以使用 TDXParams.MARKET_SH , TDXParams.MARKET_SZ 常量来代替 1 和 0 作为参数

## 08. 查询分笔成交

参数：市场代码， 股票代码，起始位置， 数量 如： 0,000001,0,10

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std') 
client.minute(symbol="000001", start=0, offset=30)
```

## 09. 查询历史分笔

参数：市场代码， 股票代码，起始位置，日期 数量 如： 0,000001,0,10,20170209

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')
client.transaction(symbol="000001", start=0, offset=10, date=20170209)
```

## 10. 公司信息目录

参数：市场代码， 股票代码， 如： 0,000001 或 1,600300

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')
client.F10C('000001')
```

## 11. 公司信息详情

参数：市场代码， 股票代码, 文件名, 起始位置， 数量, 如：0,000001,000001.txt,2054363,9221

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')
client.F10("000001", "000001.txt", 0, 100)
```

注意这里的 起始位置， 数量 参考上面接口的返回结果。

## 12. 除权除息信息

参数：市场代码， 股票代码， 如： 0,000001 或 1,600300

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')
client.xdxr(symbol="600300")
```

## 13. 读取财务信息

参数：市场代码， 股票代码， 如： 0,000001 或 1,600300

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')
client.finance(symbol="600300")
```

## 14. 读取k线信息

参数：市场代码， 开始时间， 结束时间

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')
client.k(symbol="600300", begin="2017-07-03", end="2017-07-10")
```
