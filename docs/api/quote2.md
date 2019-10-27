## 01. 获取市场代码

可以获取该api服务器可以使用的市场列表，类别等信息

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.markets()

```

## 02. 查询代码列表

参数， 起始位置， 获取数量

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.instrument(start=0, offset=100)

# 获取全部
client.instruments()
```

## 03. 市场商品数量

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.instrument_count()

```

## 04. 查询五档行情

参数 市场ID，证券代码

- 市场ID可以通过 `markets` 方法获得

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.quote(market=47, symbol="IF1709")

# 简写方式
client.quote(symbol="47#IF1709")
```

## 05. 查询分时行情

参数 市场ID，证券代码

- 市场ID可以通过 `markets` 方法获得

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.minute(market=47, symbol='IF1709')

# 简写方式
client.minute(symbol="47#IF1709")
```

## 06. 历史分时行情

参数 市场ID，证券代码，日期

- 市场ID可以通过 `markets` 方法获得
- 日期格式 YYYYMMDD 如 20170811

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.minutes(market=47, symbol='IF1709')

# 简写方式
client.minutes(symbol="47#IF1709")
```

## 07. 查询k线数据

参数： K线周期， 市场ID， 证券代码，起始位置， 数量

- K线周期参考 `mootdx.consts`
- 市场ID可以通过 `markets` 方法获得

```python
from mootdx.quotes import Quotes
from mootdx.consts import KLINE_DAILY

client.bars(category=KLINE_DAILY, market=47, symbol="47#IF1709", start=0, offset=100)

# 简写方式
client.bars(category=KLINE_DAILY, symbol="47#IF1709", start=0, offset=100)
```

## 08. 查询分笔成交

参数：市场ID，证券代码

- 市场ID可以通过 `markets` 方法获得

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.transaction(31, "00020")

# 简写方式
client.transaction("31#00020")
```

注意，这个接口最多返回`1800`条记录, 如果有超过1800条记录的请求，我们有一个start 参数作为便宜量，可以取出超过1800条记录

如期货的数据：这个接口可以取出1800条之前的记录，数量也是1800条

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.transaction(market=31, symbol='00020')


# 简写方式
client.transaction("31#00020")
```

## 09. 历史分笔成交

参数：市场ID，证券代码, 日期

- 市场ID可以通过 `markets` 方法获得
- 日期格式 YYYYMMDD 如 20170810

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.transactions(market=47, symbol='IFL0', date='20170810', start=1800)

# 简写方式
client.transaction(symbol="47#IFL0", date='20170810', start=1800)
```

