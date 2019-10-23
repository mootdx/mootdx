
# 测试最优服务器

我提供了一个命令行工具来实现简单的交互和功能演示，在安装之后，应该可以直接使用 `mootdx` 命令调用.

您可以随时使用`mootdx --help`获取接口的使用规则。


### 查看帮助

```shell
$ mootdx --help

Usage: mootdx [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose
  --help         Show this message and exit.

Commands:
  affair  财务文件下载&解析.
  bestip  测试行情服务器IP.
  quotes  读取股票在线行情数据.
  reader  读取股票本地行情数据.

```

### 执行命令

> 测试最优服务器IP，参数说明

```shell
$ mootdx bestip --help

Usage: mootdx bestip [OPTIONS]

  测试行情服务器.

Options:
  -l, --limit TEXT   显示最快前几个，默认 5.
  -t, --tofile TEXT  将数据输出到文件.
  -w, --write        将最优服务器IP写入配置文件 ~/.mootdx/config.json.
  -v, --verbose
  --help             Show this message and exit.

```

## 测试结果

> 测试命令结果，建议时常测试并加`-w`参数写入配置文件

```shell
$ mootdx bestip -v -w

124.160.88.183,7709 验证失败.
218.85.139.19,7709 验证失败.
218.85.139.20,7709 验证失败.
最优服务器:
+-----------------+-----------------+------+--------+
| Name            | Addr            | Port |   Time |
+-----------------+-----------------+------+--------+
| 北京联通主站Z2  | 202.108.253.131 | 7709 | 0.13ms |
| 安信            | 114.80.149.92   | 7709 | 0.23ms |
| 海通            | 123.125.108.90  | 7709 | 0.60ms |
| 北京联通主站Z80 | 202.108.253.139 | 80   | 0.63ms |
| 安信            | 114.80.149.91   | 7709 | 0.69ms |
+-----------------+-----------------+------+--------+

```

