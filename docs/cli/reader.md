
# 读取离线数据

`mootdx reader` 是一个命令行程序，目前功能比较简单，可以用来读取通达信导出的日线行情数据

使用方法如下：

```
Usage: mootdx reader [OPTIONS] INPUT

  通达信数据文件读取

Options:
  -o, --output TEXT
  -d, --datatype TEXT  数据文件格式，
                        - daily 代表日K线
                        - ex_daily 代表扩展行情的日线
                        - min
                       代表5分钟或者1分钟线
                        - lc 代表lc1, lc5格式的分钟线
                        - gbbq 股本变迁文件
                        -
                       block 读取板块股票列表文件
                        - customblock 读取自定义板块列表
                        -
                       history_financial 或者 hf 历史财务信息 如 gpcw20170930.dat 或者
                       gpcw20170930.zip
  --help               Show this message and exit.

```

如：

```
(C:\Anaconda3) C:\Users\Administrator&gt;mootdx reader -o f:\dt.csv -d daily C:\new_tdx\vipdoc\sz\lday\sz000001.day
写入到文件 : f:\dt.csv

```
# 读取线上数据
