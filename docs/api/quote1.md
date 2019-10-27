
# 00. 行情接口说明

下面是如何在程序里面调用本接口

首先需要引入

```python
from mootdx.quotes import Quotes

```

然后，创建对象

```python
client = Quotes.factory(market='std', multithread=True, heartbeat=True) 
```

## 01. 查询实时行情

可以获取**多**只股票的行情信息

如：

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std') 
client.quotes(symbol=["000001", "600300"])
```

注意点：非股票品种代码，有些获取的价格不是实际价格，比如可转债获取价格为实际价格 x 10。
这是可能是TDX为了防止浮点数错误，报价在传输和存储时实际都保存为整数，然后根据品种进行处理的结果。

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
client.bars(symbol='600036', category=9, offset=10)
```

## 03. 查询股票数量

sz - 深圳， sh - 上海

```python
from mootdx.quotes import Quotes
from mootdx import consts

client = Quotes.factory(market='std') 
client.stock_count(market=consts.MARKET_SH)

Out:
	19985
```

## 04. 查询股票列表

参数：市场代码, 起始位置 如： 0,0 或 1,100

```python
from mootdx.quotes import Quotes
from mootdx import consts

client = Quotes.factory(market='std') 
client.stocks(market=consts.MARKET_SH)

Out:
       code  volunit  decimal_point    name     pre_close
0    999999      100              2    上证指数   2940.921387
1    999998      100              2    Ａ股指数   3081.057129
2    999997      100              2    Ｂ股指数    264.707489
3    000001      100              2    上证指数   2940.921387
4    000002      100              2    Ａ股指数   3081.057129
5    000003      100              2    Ｂ股指数    264.707489
6    000004      100              2    工业指数   2286.899170
7    000005      100              2    商业指数   2703.876709
8    000006      100              2    地产指数   6694.932129
9    000007      100              2    公用指数   4855.400391
10   000008      100              2    综合指数   2900.845947
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
client.index(category=9, market='sz', symbol='000001', start=1, offset=2)

Out:
      open    close     high     ...              datetime  up_count  down_count
0  2952.97  2941.62  2957.30     ...      2019-10-23 15:00       381        1113
1  2944.01  2940.92  2953.04     ...      2019-10-24 15:00       715         754

[2 rows x 14 columns]
```
## 06. 查询分时行情

参数：市场代码， 股票代码， 如： 0,000001 或 1,600300

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std') 
client.minute(symbol='000001')

Out:
        price     vol
0        0.00      48
1        0.48      48
2        0.97    1688
3        0.96       8
4        0.66   -1688
5     6915.01   -6774
6     6965.03  354572
7     6965.04       0


```

## 07. 历史分时行情

参数：市场代码， 股票代码，时间 如： 0,000001,20161209 或 1,600300,20161209

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std') 
client.minutes(symbol='000001', date='20171010')

Out:
     price    vol
0    11.36  11408
1    11.38   6312
2    11.38   5023
3    11.37   3174
4    11.37   4798
5    11.39   3377
6    11.44  10392
7    11.46  11305
8    11.46   8787

```

注意，在引入 TDXParams 之后， （`from mootdx.params import TDXParams`） 我们可以使用 TDXParams.MARKET_SH , TDXParams.MARKET_SZ 常量来代替 1 和 0 作为参数

## 08. 查询分笔成交

参数：市场代码， 股票代码，起始位置， 数量 如： 0,000001,0,10

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std') 
client.transaction(symbol='600036', start=0, offset=10)

Out:
    time  price   vol  num  buyorsell
0  15:00   36.4  4097  222          2
```

## 09. 查询历史分笔

参数：市场代码， 股票代码，起始位置，日期 数量 如： 0,000001,0,10,20170209

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')
client.transactions(symbol='000001', start=0, offset=10, date='20170209')

Out:
    time  price   vol  num  buyorsell
0  15:00   36.4  4097  222          2
```

## 10. 公司信息目录

参数：市场代码， 股票代码， 如： 0,000001 或 1,600300

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')
client.F10C(symbol='000001')

Out:
    name    filename   start  length
0   最新提示  000001.txt       0    9679
1   公司概况  000001.txt    9679    8139
2   财务分析  000001.txt   17818   36701
3   股东研究  000001.txt   54519   21833
4   股本结构  000001.txt   76352    5327
5   资本运作  000001.txt   81679    3523
6   业内点评  000001.txt   85202   45843
7   行业分析  000001.txt  592660   18250
8   公司大事  000001.txt  131045  134480
9   港澳特色  000001.txt  265525   15260
10  经营分析  000001.txt  280785   16055
11  主力追踪  000001.txt  296840   56545
12  分红扩股  000001.txt  353385   93994
13  高层治理  000001.txt  447379   44723
14  龙虎榜单  000001.txt  492102   10409
15  关联个股  000001.txt  502511   90149
```

## 11. 公司信息详情

参数：市场代码， 股票代码, 文件名, 起始位置， 数量, 如：0,000001,000001.txt,2054363,9221

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')
client.F10(symbol='000001', file='000001.txt', start=0, offset=9679)

Out:
                                               value
0  ☆最新提示☆ ◇000001 平安银行 更新日期：2019-10-26◇ 港澳资讯 灵通V7...
```

注意这里的 起始位置， 数量 参考上面接口的返回结果。

## 12. 除权除息信息

参数：市场代码， 股票代码， 如： 0,000001 或 1,600300

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')
client.xdxr(symbol='600036')

Out:
    year  month  day     ...       houzongguben fenshu  xingquanjia
0   2002      4    9     ...       5.706818e+05    NaN          NaN
1   2002      7   10     ...       5.706818e+05    NaN          NaN
2   2002      8   12     ...       5.706818e+05    NaN          NaN
3   2002     12   10     ...       5.706818e+05    NaN          NaN
```

## 13. 读取财务信息

参数：市场代码， 股票代码， 如： 0,000001 或 1,600300

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')
client.finance(symbol="600300")

Out[27]:
   market    code  liutongguben   ...     weifenlirun  baoliu1  baoliu2
0       1  600300      167200.0   ...     745611.5625      0.0      6.0

[1 rows x 37 columns]
```

## 14. 读取k线信息

参数：市场代码， 开始时间， 结束时间

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')
client.k(symbol="600300", begin="2017-07-03", end="2017-07-10")

Out:
            open  close  high   ...         amount        date    code
date                            ...
2017-07-03  5.34   5.40  5.41   ...     59721688.0  2017-07-03  600300
2017-07-04  5.38   5.34  5.39   ...     44179364.0  2017-07-04  600300
2017-07-05  5.35   5.35  5.36   ...     58219360.0  2017-07-05  600300
2017-07-06  5.35   5.34  5.36   ...     59126872.0  2017-07-06  600300
2017-07-07  5.33   5.53  5.57   ...    213569888.0  2017-07-07  600300
2017-07-10  5.51   5.44  5.51   ...    121877824.0  2017-07-10  600300

[6 rows x 8 columns]
```
