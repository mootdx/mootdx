
读取通达信离线数据接口

## 读取通达信的日K线

通过下面的接口，我们可以解析通达信的日K线文件，该文件可以通过读取通达信的软件本地目录导出的数据获取，也可以从通达信的官网上下载， 如果您安装了通达信的终端，可以在安装目录下找到 `vipdoc` 子目录。

比如我的通达信客户端安装在 `c:\new_tdx` 下，

即

- `c:\new_tdx\vipdoc\sz\lday\` 下是深圳的日k线数据
- `c:\new_tdx\vipdoc\sh\lday\` 下是上海的日k线数据

该目录下每个股票为一个文件，如 `sz000001.day` 为深圳的日k行情，

### 读取行情的接口非常简单

```python
from mootdx.reader import Reader

reader = Reader.factory(market='std', tdxdir='C:/new_tdx')

# 读取日线数据
reader.daily(symbol='600036')
# 读取分钟数据
reader.minute(symbol='600036')
# 读取时间线数据
reader.fzline(symbol='600036')

输出为：

             open   high    low  close        amount     volume
date
1991-12-23  27.70  27.90  27.60  27.80  3.530600e+06     127000
1991-12-24  27.90  29.30  27.00  29.05  3.050250e+06     105000
1991-12-25  29.15  30.00  29.10  29.30  6.648170e+06     226900
1991-12-26  29.30  29.30  28.00  28.00  5.370400e+06     191800
1991-12-27  28.00  28.50  28.00  28.45  5.988725e+06     210500
...           ...    ...    ...    ...           ...        ...
2017-06-22   9.15   9.40   9.14   9.25  1.325211e+09  142695815
2017-06-23   9.23   9.27   9.16   9.25  5.383036e+08   58400441
2017-06-26   9.26   9.40   9.26   9.30  6.637629e+08   71076995

[6031 rows x 6 columns]

```

## 读取扩展行情的日线（如期货，期权，现货等）

```python

from mootdx.reader import Reader

reader = Reader.factory(market='ext', tdxdir='c:/new_tdx/vipdoc')
reader.daily(symbol='29#A1801')

Out[4]:
              open    high     low   close  amount  volume  jiesuan
date
2017-08-07  3830.0  3936.0  3826.0  3925.0  167038  224516   3881.0
2017-08-08  3926.0  3990.0  3921.0  3951.0  188460  256984   3958.0
2017-08-09  3951.0  3997.0  3951.0  3982.0  194150  157330   3976.0
2017-08-10  3978.0  4015.0  3970.0  3995.0  206944  174878   3993.0
2017-08-11  3997.0  4017.0  3927.0  3954.0  202010  258036   3971.0

```

## 读取分钟线

> 读取通达信的分钟K线（目前支持1，5分钟k线）

分钟线有两种格式，第一种是`.1` `.5` 为后缀的

```python
from mootdx.reader import Reader
reader = Reader.factory(market='ext', tdxdir='c:/new_tdx')
reader.minute(symbol='000001', suffix='1') # suffix = 1 一分钟，5 五分钟

Out[2]:
                        open     high      low    close        amount  \
date
2015-07-09 09:35:00  3432.45  3454.14  3374.32  3423.61  6.189348e+10
2015-07-09 09:40:00  3420.56  3424.16  3395.07  3396.33  2.341652e+10

                        volume
date
2015-07-09 09:35:00  618934736
2015-07-09 09:40:00  234165181

```

还有一种为 `.lc1` `.lc5` 后缀的

```python
from mootdx.reader import Reader
reader = Reader.factory(market='ext', tdxdir='c:/new_tdx')
reader.minute(symbol='000001')

open       high        low      close       amount  \
date                                                                           
2017-07-26 09:35:00  10.920000  10.990000  10.860000  10.940000  118572536.0   
2017-07-26 09:40:00  10.929999  10.990000  10.910000  10.969999   43107384.0   
2017-07-26 09:45:00  10.969999  11.050000  10.969999  11.050000   40586544.0   
2017-07-26 09:50:00  11.050000  11.130000  11.010000  11.120000  100486624.0   
2017-07-26 09:55:00  11.110000  11.179999  11.099999  11.179999   78094816.0   
....
....
...

```

## 读取板块信息

文件位置参考： [http://blog.sina.com.cn/s/blog_623d2d280102vt8y.html](http://blog.sina.com.cn/s/blog_623d2d280102vt8y.html)

样例代码：

```python
from mootdx.reader import Reader
reader = Reader.factory(market='ext', tdxdir='c:/new_tdx')
reader.block(market='zs', group=BlockReader_TYPE_GROUP)

blockname  block_type  code_index    code
0        沪深300           2           0  000001
1        沪深300           2           1  000002
2        沪深300           2           2  000008
3        沪深300           2           3  000009


# 分组格式
df2 = BlockReader().get_df("/Users/rainx/tmp/block_zs.dat", BlockReader_TYPE_GROUP)
print(df2)

blockname  block_type  stock_count  \
0       重点沪指           2            0   
1      沪深300           2          300   
2       深证成指           2           40   
3       中小板指           2          100   

code_list  
0                                                      
1   000001,000002,000008,000009,000060,000063,0000...  
2   000001,000002,000063,000069,000100,000157,0001...  
3   002001,002004,002007,002008,002010,002013,0020...

```

## 读取自定义板块信息

> 读取通达信的自定义板块信息文件夹

在通达信客户端备份自定义板块数据，设置-->数据维护工具-->数据备份，备份后会生出类似TdxBak_20171011/blocknew的文件夹，然后使用如下代码读取：

```python
# 默认扁平格式
df = CustomerBlockReader().get_df(&amp;apos;C:/Users/fit/Desktop/TdxBak_20171011/blocknew&amp;apos;)
print(df)

    blockname block_type  code_index     code
0          领袖         LX           1  1600516
1          领袖         LX           2  0300678
2          领袖         LX           3  0300675
3          领袖         LX           4  1600230
4          领袖         LX           5  0002497
5          领袖         LX           6  0002460
6          领袖         LX           7  0000807
7          领袖         LX           8  1600874

#分组格式
df = CustomerBlockReader().get_df(&amp;apos;C:/Users/fit/Desktop/TdxBak_20171011/blocknew&amp;apos;, BlockReader_TYPE_GROUP)
print(df)

   blockname block_type  stock_count  \
0         领袖         LX           20   
1         核心         HX           20   
2         潜力         QL           11

                                            code_list  
0   1600516,0300678,0300675,1600230,0002497,000246...  
1   1603501,0300597,0002467,0300081,0002194,000086...  
2   1600686,0300648,1600476,0300036,1603066,030062...

```
