# 命令使用说明

`mootdx quotes` 是一个命令行程序，目前功能比较简单，可以用来读取TDX导出的日线行情数据

使用方法如下：

```shell
mootdx quotes --help

Usage: mootdx quotes [OPTIONS]

  读取股票在线行情数据.

Options:
  -o, --output TEXT  输出文件, 支持CSV, HDF5, Excel等格式.
  -s, --symbol TEXT  股票代码.
  -a, --action TEXT  操作类型 (daily:日线, minute:一分钟线, fzline:五分钟线).
  -m, --market TEXT  证券市场, 默认 std (std: 标准股票市场, ext: 扩展市场).
  --help             Show this message and exit.
```

# 读取日线数据

读取行情并写入到文件: minute.csv

```shell
mootdx quotes -s 600000 -a minute -o minute.csv
```
