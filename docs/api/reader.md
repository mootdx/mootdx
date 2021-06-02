
## 00. 离线数据说明

通过下面的接口，我们可以解析通达信的日K线文件，该文件可以通过读取通达信的软件本地目录导出的数据获取，也可以从通达信的官网上下载， 如果您安装了通达信的终端，可以在安装目录下找到 `vipdoc` 子目录。

比如我的通达信客户端安装在 `c:\new_tdx` 下，

即

- `C:/new_tdx/vipdoc/sz/lday/` 下是深圳的日k线数据
- `C:/new_tdx/vipdoc/sh/lday/` 下是上海的日k线数据

该目录下每个股票为一个文件，如 `sz000001.day` 为深圳的日k行情，

### 01. 读取行情接口

```python
from mootdx.reader import Reader
reader = Reader.factory(market='std', tdxdir='C:/new_tdx')

# 读取日线数据
reader.daily(symbol='600036')
# 读取1分钟数据
reader.minute(symbol='600036')
# 读取5分钟数据
reader.fzline(symbol='600036')
```

## 02. 读取扩展行情

> 读取扩展行情的日线（如期货，期权，现货等）

```python

from mootdx.reader import Reader

reader = Reader.factory(market='ext', tdxdir='c:/new_tdx')
reader.daily(symbol='29#A1801')
```

## 03. 历史分钟数据

> 读取通达信的分钟K线（目前支持1，5分钟k线）

分钟线有两种格式，第一种是`.1` `.5` 为后缀的, 还有一种为 `.lc1` `.lc5` 后缀的.
不过不用考虑，接口会自动判断

```python
from mootdx.reader import Reader
reader = Reader.factory(market='std', tdxdir='c:/new_tdx')
reader.minute(symbol='000001', suffix='1') # suffix = 1 一分钟，5 五分钟
```

扩展数据接口读取方式

```python
from mootdx.reader import Reader
reader = Reader.factory(market='ext', tdxdir='c:/new_tdx')
reader.minute(symbol='000001', suffix = '1') # suffix = 1 一分钟，5 五分钟
```

## 04. 读取板块信息

文件位置参考： [http://blog.sina.com.cn/s/blog_623d2d280102vt8y.html](http://blog.sina.com.cn/s/blog_623d2d280102vt8y.html)

样例代码：

```python
from mootdx.reader import Reader
reader = Reader.factory(market='ext', tdxdir='c:/new_tdx')
reader.block(symbol='block_zs', group=True)
```

```python
# 分组格式
reader.block(symbol='block_zs', group=True)
```

## 05. 自定义板块数据

> 读取通达信的自定义板块信息文件夹

在通达信客户端备份自定义板块数据，设置-->数据维护工具-->数据备份，备份后会生出类似TdxBak_20171011/blocknew的文件夹，然后使用如下代码读取：

```python
# 默认扁平格式
from mootdx.reader import Reader
reader = Reader.factory(market='std', tdxdir='C:/new_tdx')
reader.block(symbol='block_zs', custom=True)

#分组格式
reader.block(symbol='block_zs', custom=True, group=True)
```
