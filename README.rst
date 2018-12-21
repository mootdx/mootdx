
通达信数据读取
==============================


.. image:: https://img.shields.io/pypi/v/mootdx.svg
        :target: https://pypi.python.org/pypi/mootdx

.. image:: https://img.shields.io/travis/bopo/mootdx.svg
        :target: https://travis-ci.org/bopo/mootdx

.. image:: https://readthedocs.org/projects/mootdx/badge/?version=latest
        :target: https://mootdx.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/bopo/mootdx/shield.svg
     :target: https://pyup.io/repos/github/bopo/mootdx/
     :alt: Updates



* 开源协议: MIT license
* 在线文档: https://mootdx.readthedocs.io.

安装方法
--------

::

	# PIP 自动安装方法
	pip install mootdx

	# 手动下载源码安装
	git clone https://github.com/bopo/mootdx.git 
	cd mootdx
	python setup.py install


使用说明
--------
命令行工具

::
	
	mootdx --help

	Usage: mootdx [OPTIONS] COMMAND [ARGS]...

	Options:
	  -v, --verbose
	  --help         Show this message and exit.

	Commands:
	  affair  财务文件下载&解析.
	  quotes  读取股票行情数据.
	  server  测试行情服务器.

使用最快的服务器

:: 

	# -w 参数是写入配置文件
	mootdx server -w 


通达信离线数据读取

::

	from mootdx.reader import Reader

	# market 参数 std 为标准市场(就是股票), ext 为扩展市场(期货，黄金等)
	# tdxdir 是通达信的数据目录, 根据自己的情况修改
	reader = Reader.factory(market='std', tdxdir='./tests/data')
	result = reader.daily(symbol='600036')
	result = reader.minute(symbol='600036')
	result = reader.fzline(symbol='600036')


通达信离线行情读取

::

	from mootdx.quotes import Quotes

	# 标准市场
	client = Quotes.factory(market='std', multithread=True, heartbeat=True)

	# k 线数据
	client.bars(symbol='600036', category=9, offset=10)

	# 指数
	client.index(symbol='000001', category=9)

	# 分钟
	client.minute(symbol='000001')


通达信财务数据读取

::

	from mootdx.affairs import Affairs

	# 远程文件列表
	files = Affairs.files()

	# 下载单个
	Affairs.fetch(downdir='tmp', filename='gpcw19960630.zip')

	# 下载全部
	Affairs.parse(downdir='tmp')


版本更新
--------

* 更新了最佳服务器选择问题
* 修改了 PIP 安装程序问题
* 本程序只支持 python3.
* 通达信客户端文件转换
* 通达信在线行情下载

贡献名单
---------

- bopo.wang

