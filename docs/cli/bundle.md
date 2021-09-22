# 命令使用说明

`mootdx bundle` 是一个命令行程序，目前功能比较简单，可以用来读取TDX导出的日线行情数据

使用方法如下：

```shell
mootdx bundle --help

Usage: mootdx bundle [OPTIONS]

  批量下载行情数据.

Options:
  -o, --output TEXT     转存文件目录.
  -s, --symbol TEXT     股票代码. 多个用,隔开
  -a, --action TEXT     操作类型 (daily: 日线, minute: 一分钟线, fzline: 五分钟线).
  -m, --market TEXT     证券市场, 默认 std (std: 标准股票市场, ext: 扩展市场).
  -e, --extension TEXT  转存文件的格式, 支持 CSV, HDF5, Excel, JSON 等格式.
  --help                Show this message and exit.
```

# 读取日线数据

读取行情并写入到文件: minute.csv

```shell
mootdx bundle -s 600000 -a minute -o minute.csv
```
