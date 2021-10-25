通达信数据读取接口
==================

.. image:: https://badge.fury.io/py/mootdx.svg
   :target: http://badge.fury.io/py/mootdx

.. image:: https://img.shields.io/travis/bopo/mootdx.svg
        :target: https://travis-ci.org/mootdx/mootdx

.. image:: https://readthedocs.org/projects/mootdx/badge/?version=latest
        :target: https://mootdx.readthedocs.io/zh/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/mootdx/mootdx/shield.svg
     :target: https://pyup.io/repos/github/mootdx/mootdx/
     :alt: Updates

如果喜欢本项目可以在右上角给颗⭐！你的支持是我最大的动力😎！

* 开源协议: MIT license
* 在线文档: https://mootdx.readthedocs.io
* 国内镜像: https://gitee.com/ibopo/mootdx
* 项目仓库: https://github.com/mootdx/mootdx

版本更新(倒序)
--------------

版本更新日志: https://mootdx.readthedocs.io/zh_CN/latest/chlog/


运行环境
---------

* 操作系统: Windows / MacOS / Linux 都可以运行.
* Python: 3.5 以及以上版本, 不支持 python2.
* 依赖库: PyTdx>=1.67


安装方法
---------

::

    # PIP 自动安装方法
    pip install mootdx

    # 手动下载源码安装
    git clone --depth=1 https://github.com/bopo/mootdx.git
    cd mootdx
    python setup.py install


使用说明
---------

命令行工具

::

    mootdx --help

    Usage: mootdx [OPTIONS] COMMAND [ARGS]...

    Options:
      -v, --verbose
      --help         Show this message and exit.

    Commands:
      affair  财务文件下载&解析.
      bestip  测试行情服务器.
      quotes  读取股票在线行情数据.
      reader  读取股票本地行情数据.

使用最快的服务器

::

    # -w 参数是写入配置文件
    mootdx bestip -w -v


通达信离线数据读取

::

    from mootdx.reader import Reader

    # market 参数 std 为标准市场(就是股票), ext 为扩展市场(期货，黄金等)
    # tdxdir 是通达信的数据目录, 根据自己的情况修改

    reader = Reader.factory(market='std', tdxdir='C:/new_tdx')

    # 读取日线数据
    reader.daily(symbol='600036')

    # 读取分钟数据
    reader.minute(symbol='600036')

    # 读取时间线数据
    reader.fzline(symbol='600036')



通达信线上行情读取

::

    from mootdx.quotes import Quotes

    # 标准市场
    client = Quotes.factory(market='std', multithread=True, heartbeat=True)

    # k 线数据
    client.bars(symbol='600036', frequency=9, offset=10)

    # 指数
    client.index(symbol='000001', frequency=9)

    # 分钟
    client.minute(symbol='000001')


通达信财务数据读取

::

    from mootdx.affair import Affair

    # 远程文件列表
    files = Affair.files()

    # 下载单个
    Affair.fetch(downdir='tmp', filename='gpcw19960630.zip')

    # 下载全部
    Affair.parse(downdir='tmp')


加微信交流
-----------

.. image:: docs/img/IMG_2851.JPG
        :width: 130 px
        :align: left
