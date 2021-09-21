## 扩展行情接口

> 注意：扩展市场目前已经失效无法使用

## 01. 获取市场代码

可以获取该api服务器可以使用的市场列表，类别等信息

** 调用方法：**

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext')
client.markets()

```

> 注意点：非股票品种代码，有些获取的价格不是实际价格，比如可转债获取价格为实际价格 x 10。
> 这是可能是TDX为了防止浮点数错误，报价在传输和存储时实际都保存为整数，然后根据品种进行处理的结果。

## 02. 查询代码列表

** 参数说明: **

- start: 起始位置.
- offset: 获取数量.

** 调用方法：**

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext')
client.instrument(start=0, offset=100)

# 获取全部
client.instruments()
```

## 03. 市场商品数量

** 调用方法：**

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext')
client.instrument_count()

```

## 04. 查询五档行情

** 参数说明: **

- market: 市场代码.
- symbol: 证券代码.

** 调用方法：**

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext')
client.quote(market=47, symbol="IF1709")

# 简写方式
client.quote(symbol="47#IF1709")
```

## 05. 查询分时行情

** 参数说明: **

- market: 市场代码. 市场代码可以通过 `markets` 方法获得
- symbol: 证券代码.

** 调用方法：**

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext')
client.minute(market=47, symbol='IF1709')

# 简写方式
client.minute(symbol="47#IF1709")
```

## 06. 历史分时行情

** 参数说明: **

- market: 市场代码. 场ID可以通过 `markets` 方法获得
- symbol: 证券代码

** 调用方法：**

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext')
client.minutes(market=47, symbol='IF1709')

# 简写方式
client.minutes(symbol="47#IF1709")
```

## 07. 查询k线数据

** 参数说明: **

- frequency: K线周期参考 `mootdx.consts`
- market: 市场代码. 场ID可以通过 `markets` 方法获得
- symbol: 证券代码
- start: 起始位置
- offset: 数量

** 调用方法：**

```python
from mootdx.quotes import Quotes
from mootdx.consts import KLINE_DAILY

client = Quotes.factory(market='ext')
client.bars(frequency=KLINE_DAILY, market=47, symbol="47#IF1709", start=0, offset=100)

# 简写方式
client.bars(frequency=KLINE_DAILY, symbol="47#IF1709", start=0, offset=100)
```

## 08. 查询分笔成交

** 参数说明: **

- market: 市场代码. 场ID可以通过 `markets` 方法获得
- symbol: 证券代码

** 调用方法：**

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext')
client.transaction(31, "00020")

# 简写方式
client.transaction("31#00020")
```

注意，这个接口最多返回`1800`条记录, 如果有超过1800条记录的请求，我们有一个start 参数作为便宜量，可以取出超过1800条记录

如期货的数据：这个接口可以取出1800条之前的记录，数量也是1800条

** 调用方法：**

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext')
client.transaction(market=31, symbol='00020')

# 简写方式
client.transaction("31#00020")
```

## 09. 历史分笔成交

** 参数说明: **

- market: 市场代码. 场ID可以通过 `markets` 方法获得
- symbol: 证券代码
- date: 日期. 日期格式 YYYYMMDD 如 20170811
- start: 起始位置
- offset: 数量

** 调用方法：**

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext')
client.transactions(market=47, symbol='IFL0', date='20170810', start=1800)

# 简写方式
client.transaction(symbol="47#IFL0", date='20170810', start=1800)
```
