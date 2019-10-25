
# 扩展行情接口API

首先需要引入

```python
from mootdx.quotes import Quotes
```

然后，创建对象

```python
client = Quotes.factory(market='ext', multithread=True, heartbeat=True)
```

- 参数一般性约定

一般来说，股票代码和文件名称使用字符串类型，其它参数都使用数值类型

## 01. 获取市场代码

可以获取该api服务器可以使用的市场列表，类别等信息

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.markets()

```

返回结果 `api.to_df(api.get_markets())` 一般某个服务器返回的类型比较固定，该结果可以缓存到本地或者内存中。

```
2017-07-31 21:22:06,067 - PYTDX - INFO - 获取市场代码
    market  category    name short_name
0        1         1     临时股         TP
1        4        12  郑州商品期权         OZ
2        5        12  大连商品期权         OD
3        6        12  上海商品期权         OS
4        8        12  上海个股期权         QQ
5       27         5    香港指数         FH
6       28         3    郑州商品         QZ
7       29         3    大连商品         QD
8       30         3    上海期货         QS
9       31         2    香港主板         KH
10      32         2    香港权证         KR
11      33         8   开放式基金         FU
12      34         9   货币型基金         FB
13      35         8  招商理财产品         LC
14      36         9  招商货币产品         LB
15      37        11    国际指数         FW
16      38        10  国内宏观指标         HG
17      40        11   中国概念股         CH
18      41        11  美股知名公司         MG
19      43         1   B股转H股         HB
20      44         1    股份转让         SB
21      47         3    股指期货         CZ
22      48         2   香港创业板         KG
23      49         2  香港信托基金         KT
24      54         6   国债预发行         GY
25      60         3  主力期货合约         MA
26      62         5    中证指数         ZZ
27      71         2     港股通         GH

```

## 02. 查询代码列表

参数， 起始位置， 获取数量

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.instrument(0, 100)

```

Dem0o. <img alt="get_list_demo" src="assets/mootdx_exhq-bf0d0.png"/>

## 03. 市场商品数量

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.instruments()

```

## 04. 查询五档行情

参数 市场ID，证券代码

- 市场ID可以通过 `get_markets` 获得

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.quote(47, "IF1709")

```

## 05. 查询分时行情

参数 市场ID，证券代码

- 市场ID可以通过 `get_markets` 获得

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.minute(47, "IF1709")
```

## 06. 历史分时行情

参数 市场ID，证券代码，日期

- 市场ID可以通过 `get_markets` 获得
- 日期格式 YYYYMMDD 如 20170811

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.history(31, "00020", 20170811)
```

## 07. 查询k线数据

参数： K线周期， 市场ID， 证券代码，起始位置， 数量

- K线周期参考 `TDXParams`
- 市场ID可以通过 `get_markets` 获得

```python
from mootdx.quotes import Quotes
from mootdx.consts import KLINE_DAILY

client.bars(KLINE_DAILY, 8, "10000843", 0, 100)
```

## 08. 查询分笔成交

参数：市场ID，证券代码

- 市场ID可以通过 `get_markets` 获得

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.transaction(31, "00020")
```

注意，这个接口最多返回`1800`条记录, 如果有超过1800条记录的请求，我们有一个start 参数作为便宜量，可以取出超过1800条记录

如期货的数据：这个接口可以取出1800条之前的记录，数量也是1800条

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.transactions(31, "00020", '20170810', offset=1800)
```

## 09. 历史分笔成交

参数：市场ID，证券代码, 日期

- 市场ID可以通过 `get_markets` 获得
- 日期格式 YYYYMMDD 如 20170810

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='ext') 
client.transactions(31, "00020", 20170810)
```

