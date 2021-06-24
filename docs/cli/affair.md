# 命令行工具说明

## 00. 命令行的帮助选项

```shell
mootdx affair --help

Usage: mootdx affair [OPTIONS]

  财务文件下载&解析.

Options:
  -p, --parse TEXT    要解析文件名
  -l, --files         列出文件列表
  -f, --fetch TEXT    下载财务文件的文件名
  -a, --downall       下载全部文件
  -o, --output TEXT   输出文件, 支持 CSV, HDF5, Excel, JSON 等格式.
  -d, --downdir TEXT  下载文件目录
  -v, --verbose
  --help              Show this message and exit.
```

## 01. 列出所有财务文件

```shell
mootdx affair -l

+------------------+----------+----------------------------------+
| filename         | filesize | hash                             |
+------------------+----------+----------------------------------+
| gpcw20191231.zip | 165      | b590fc5fa3a6ec6ab5d881c31e1d71a5 |
| gpcw20190930.zip | 735575   | 16e8f046362e951d154b1f5290137845 |
| gpcw20190630.zip | 3213061  | 13d2729685d65efebb0d6b47c4c16b40 |
| gpcw20190331.zip | 2859099  | 95724f55c9a20be3c7bd1cea95919ed8 |
| gpcw20181231.zip | 3274511  | 585ffa351f4060e6274bdfb9d36de097 |
| gpcw20180930.zip | 2927452  | 4f463b8536cea8fcaaec90512a562dae |
| gpcw20180630.zip | 3085199  | a6381831231a782cf193285b6fb4b22d |
| gpcw20180331.zip | 2722534  | 0835660cce80028fd59131e7c5f5f75e |
| gpcw20171231.zip | 3188864  | 572f1c558cf48e149d7e065aba5fe787 |

```

## 02. 按文件名下载文件

> 文件名由上面方法获取

```shell
mootdx affair -f gpcw20191231.zip

Downloaded 165, Total is 0
```

## 03. 批量下载全部文件

> 增加快捷方式 `mootdx affair -a`

```shell
mootdx affair -f all

Downloaded 165, Total is 0
Downloaded 30000, Total is 0
Downloaded 60000, Total is 0
Downloaded 90000, Total is 0

....

```

## 04. 按文件名解析文件

> 文件名由列表方法获取

```shell
mootdx affair -p gpcw20000930.zip

        report_date  col1  col2  ...        col313   col314        col315
code                             ...
600306     20000930   0.0   0.0  ... -4.039810e+34  31201.0 -4.039810e+34
600565     20000930   0.0   0.0  ... -4.039810e+34  81028.0 -4.039810e+34

[2 rows x 316 columns]
```
