# 命令行使用说明

`mootdx reader` 是一个命令行程序，目前功能比较简单，可以用来读取TDX导出的日线行情数据

使用方法如下：

```
mootdx reader --help

Usage: mootdx reader [OPTIONS]

  读取股票本地行情数据.

Options:
  -d, --tdxdir TEXT  TDX数据目录.
  -s, --symbol TEXT  股票代码.
  -a, --action TEXT  操作类型 (daily:日线, minute:一分钟线, fzline:五分钟线).
  -m, --market TEXT  证券市场, 默认 std (std: 标准股票市场, ext: 扩展市场).
  -o, --output TEXT  输出文件, 支持CSV, HDF5, Excel等格式.
  --help             Show this message and exit.

```

# 读取日线数据

`-o` 参数导出数据

```shell
mootdx reader --tdxdir ../fixtures -s 600000 -a daily -o dt.csv

写入到文件 : dt.csv

```

# 读取分钟数据

`-o` 参数导出数据

```shell
mootdx reader --tdxdir ../fixtures -s 600000 -a minute -o dt.csv

写入到文件 : dt.csv

```

# 读取5分钟数据

`-o` 参数导出数据

```shell
mootdx reader --tdxdir ../fixtures -s 600000 -a fzline -o dt.csv

写入到文件 : dt.csv

```
