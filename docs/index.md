# 项目概述

Mootdx 是一款纯 Python 语言开发的类似 TDX 的行情数据接口的实现。

- 在线文档: [https://mootdx.readthedocs.io](https://mootdx.readthedocs.io)
- 国内镜像: [https://gitee.com/ibopo/mootdx](https://gitee.com/ibopo/mootdx)
- 项目仓库: [https://github.com/mootdx/mootdx](https://github.com/mootdx/mootdx)

## 项目特点

- 基于 `pytdx` 二次封装。
- 完全支持 `3.6+`
- 支持全平台 `Windows / MacOS / Linux`
- 更加友好的API接口
- 自动匹配最优服务器

## 运行环境

- 操作系统: `Windows / MacOS / Linux` 都可以运行.
- Python: `3.6` 以及以上版本, 不在支持`python2`.
- 依赖库: `pytdx>=1.67` (之后会转向使用`tdxpy`)

## 快速安装

```shell
pip install -U mootdx
```

## 多种运行

我们提供了方便命令行调试和导出数据的命令行工具。
