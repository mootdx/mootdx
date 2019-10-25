
# 行情接口API

下面是如何在程序里面调用本接口

首先需要引入

```python
from mootdx.quotes import Quotes
```

然后，创建对象

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std', multithread=True, heartbeat=True) 

```


## 参数一般性约定

一般来说，股票代码和文件名称使用字符串类型，其它参数都使用数值类型


## 多线程支持

由于Python的特性，一般情况下，不太建议使用多线程代码，如果需要并发访问，建议使用多进程来实现，如果要使用多线程版本，请在初始化时设置multithread参数为True

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std', multithread=True, heartbeat=True) 
```

## 心跳包

由于长时间不与服务器交互，服务器将关闭连接，所以我们实现了心跳包的机制，可以通过

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std', heartbeat=True)
```

设置心跳包，程序会启动一个心跳包发送线程，在空闲状态下隔一段时间发送一个心跳包，注意，打开heartbeat=True选项的同时会自动打开multithread=True

## 抛出异常

我们的错误处理有两套机制，根据TdxHq_API 构造函数里的 `raise_exception` 参数来确定，如果

```python
# 默认情况
from mootdx.quotes import Quotes

client = Quotes.factory(market='std', raise_exception=True)
```

如果在调用connect 的时候，失败会返回`false`, 调用普通接口时候，如果出错的情况返回`None`

如果

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std', raise_exception=True)
```

如果在调用connect 的时候，失败会抛出`TdxConnectionError`异常, 调用普通接口时候，如果出错的情况抛出`TdxFunctionCallError`异常

## 重连机制

在调用函数的时候，如果服务器连接断开或者其它的异常情况下，为了保证在偶发的连接断开下自动重连并重新请求数据。关于重试的周期和次数，我们通过一个自定义的类实现，你可以实现自己的重试策略

如果开启的话，需要

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std', auto_retry=True)
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

## 行情服务器列表

为了方便连接服务器，我把一些常用的服务器列表整理到到 `hosts.py` 文件中. 在程序中可以通过

```python
from mootdx.consts import hq_hosts, ex_hosts

print(hq_hosts, ex_hosts)
```
