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

因最近版本迭代比较频繁之后的版本更新日志将合并到文档中

版本修改日志: https://mootdx.readthedocs.io/zh_CN/latest/chlog/

* (2021-09-08) 解决行数数据访问服务器经常超时而返回空数据问题
* (2021-09-08) 增加同花顺复权数据接口 (可查看文档`辅助函数`章节)
* (2021-09-08) 修复分钟线数据读取bug (感谢 wangjild 的帮助)
* 更新部分文档
* 优化行情服务器连接，性能更好更快
* 修改测试最快服务器方式，之后不需要命令行直接可以使用
* 增加自定义板块的添加数据功能
* 增加一个获取复权因子接口
* 修复科创板行情数据无法下载问题
* 修复本地数据读取路径错误问题
* 增加扩展数据本地分钟线数据读取
* 修复本地标准市场和扩展市场不能读取问题
* 修改科创板无法获取数据问题(感谢 bopomofo 的鼎力支持)
* 修改缺少依赖的问题
* 删除过期功能(交易服务等)
* 可转债历史数据获取识别(添加113开头).
* 修正转债数据无法获取问题.
* 修改获取股票数据接口(自动全部获取).
* 修改指数数据接口，市场参数错误。
* 修复财务数据无法下载问题.
* 更新了详细的文档.
* 多种线路配置方案. (配置文件, 环境变量等).
* 重写了专业财务数据接口.
* 更新了最佳服务器选择问题.
* 修改了 PIP 安装程序问题.
* 本程序全面支持 python3.
* 通达信客户端文件转换.
* 通达信在线行情下载.


运行环境
---------

* 操作系统: Windows / MacOS / Linux 都可以运行.
* Python: 3.5 以及以上版本, 不支持 python2.
* 依赖库: pytdx>=1.67


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
