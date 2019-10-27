
# 读取离线数据

`mootdx reader` 是一个命令行程序，目前功能比较简单，可以用来读取通达信导出的日线行情数据

使用方法如下：

```
Usage: mootdx reader [OPTIONS]

  读取股票本地行情数据.

Options:
  -d, --tdxdir TEXT  通达信数据目录
  -s, --symbol TEXT  股票代码
  -a, --action TEXT  操作类型 (daily:日线, minute:一分钟线, fzline:五分钟线)
  -m, --market TEXT  证券市场, 默认 std (std: 标准股票市场, ext: 扩展市场)
  -o, --output TEXT  输出文件, 支持csv, HDF5, Excel等格式.
  --help             Show this message and exit.

```

如：

```
(C:\Anaconda3) C:\Users\Administrator&gt;mootdx reader -o f:\dt.csv -d daily C:\new_tdx\vipdoc\sz\lday\sz000001.day
写入到文件 : f:\dt.csv

```
# 读取线上数据
