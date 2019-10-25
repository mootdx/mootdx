## 多线程支持

由于Python的特性，一般情况下，不太建议使用多线程代码，如果需要并发访问，建议使用多进程来实现，如果要使用多线程版本，请在初始化时设置`multithread`参数为`True`

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std', multithread=True, heartbeat=True) 
```

## 心跳包机制

由于长时间不与服务器交互，服务器将关闭连接，所以我们实现了心跳包的机制，可以通过

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std', heartbeat=True)
```

设置心跳包，程序会启动一个心跳包发送线程，在空闲状态下隔一段时间发送一个心跳包，注意，打开`heartbeat=True`选项的同时会自动打开`multithread=True`


## 服务器列表

为了方便连接服务器，我把一些常用的服务器列表整理到到 `hosts.py` 文件中. 在程序中可以通过

```python
from mootdx.consts import hq_hosts, ex_hosts

print(hq_hosts, ex_hosts)
```
