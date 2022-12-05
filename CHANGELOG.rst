Changelog
=========


v0.9.11 (2022-12-05)
--------------------
- Fix bugs. [bopo]

- Update docs. [bopo]

- Docs. [bopo]

- 增加复权缓存, 调整依赖版本, 修改若干小问题. [bopo]


v0.9.10 (2022-12-05)
--------------------
- 增加复权缓存, 调整依赖版本. [bopo]


v0.9.9 (2022-11-28)
-------------------
- Fix setup bug. [bopo]


v0.9.8 (2022-11-28)
-------------------
- Fix bugs. [bopo]

- Update comit. [bopo]

- Update comit. [bopo]

- Clear codes. [bopo]

- Clear codes. [bopo]


v0.9.7 (2022-11-24)
-------------------
- Update comit. [bopo]

- Update connect2. [bopo]

- Update makefile. [bopo]

- Added poetry file. [bopo]

- Added poetry file. [bopo]

- Added poetry file. [bopo]


v0.9.6 (2022-11-23)
-------------------
- Update bestip. [bopo]


v0.9.5 (2022-11-23)
-------------------
- Update bestip. [bopo]


v0.9.4 (2022-11-23)
-------------------
- Update bestip. [bopo]

- Update bestip. [bopo]

- Update bestip. [bopo]


v0.9.3 (2022-11-23)
-------------------
- Update commit. [bopo]

- Clear codes. [bopo]

- Clear codes. [bopo]

- Clear tests. [bopo]

- Fixed bugs. [bopo]


v0.9.2 (2022-11-13)
-------------------
- Update setup.cfg. [bopo]

- Update fixtures. [bopo]

- Update logger. [bopo]

- Reader.py 关于通达信特有指数的数据获取修改 #23. [bopo]

- Modify parse. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update commit. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Add readme.md. [bopo]

- Remove loguru. [bopo]

- Remove loguru. [bopo]

- Remove simplejson. [bopo]

- Remove simplejson. [bopo]

- Remove simplejson. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Clean code. [bopo]

- Pytdx -> tdxpy. [bopo]

- Pytdx -> tdxpy. [bopo]

- Update commit. [bopo]

- To_data empty value. [bopo]

- 本地数据日线复权. [bopo]

- 本地数据日线复权. [bopo]

- 本地数据日线复权. [bopo]

- Add: 手动指定市场服务器IP. [bopo]

- Update commit. [bopo]

- Fmt code. [bopo]

- Update makfile. [bopo]

- Update commit. [bopo]

- Update tests. [bopo]

- Fix httpx 0.23. [bopo]

- Add .drone.yml. [bopo]

- Sentry. [bopo]


v0.9.1 (2022-05-14)
-------------------
- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update README.rst. [bopo]

- Update README.rst. [bopo]


v0.9.0 (2022-05-13)
-------------------
- Update README.rst. [bopo]

- Update README.rst. [bopo]

- V0.9.0. [bopo]

  * 自定义板块函数调整, 添加增、删、改、查操作
  * 日志等级调整为自行可配置(之前有反馈说日志等级太低, 太多无用日志，影响性能) 构造函数调整
  * 调整K线数据数据频次参数(frequency)的赋值方式, 原数字方式改成字符, 例如(原15分钟线值`1`改为`15m`)
  * 增加服务器IP功能, 构造函数里添加 `server`参数 例如：`client = Quotes.factory(market='std', server=('127.0.0.0',7727), verbose=0, quiet=True)`
  * 日志过滤的调整
  * 恢复了holiday2
  * 财务数据的表头转为中文, 使用时更加直观
  * 复权算法, 已经修复
- Xdxr 增加当日缓存，加速. [bopo]

- Update todo.md. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- 更block. [bopo]

- 更改json成simplejson. [bopo]

- 更改json成simplejson. [bopo]

- 更新命令行的一个卡顿小问题. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update tests. [bopo]

- √ [文档/测试] 板块读取函数调整, 详情请查看文档 √ [文档] 日志等级调整为自行可配置(之前有反馈说日志等级太低, 太多无用日志，影响性能) 构造函数调整 √ [文档] 调整K线数据数据频次参数(frequency)的赋值方式, 原数字方式改成字符, 例如(原15分钟线值`1`改为`15m`) √ [功能] 增加服务器IP功能, 构造函数里添加 √ [功能] 日志过滤的调整 √ [恢复] 恢复了holiday2 √ [调整] 财务数据的 columns 转中文 √ [调整] 复权算法, 自动结果. [bopo]

- 更新执行脚本. [bopo]

  update commit

  update commit

  - 新版自定义板块操作
  - 对应文档更新

  - 新版自定义板块操作
  - 对应文档更新

  更新命令行的一个卡顿小问题

  更改json成simplejson

  更改json成simplejson

  更block

  Bump version: 0.8.12 → 0.8.13
- Clean code. [bopo]


v0.8.14 (2022-05-08)
--------------------
- Update commit. [bopo]

- - 复权试验. [Yi Wang B]

- Update .readthedocs.yaml. [bopo]

- Update .readthedocs.yaml. [bopo]

- Update .readthedocs.yaml. [bopo]

- Update .readthedocs.yaml. [bopo]


v0.8.13 (2022-05-07)
--------------------
- 更block. [bopo]

- 更改json成simplejson. [bopo]

- 更改json成simplejson. [bopo]

- 更新命令行的一个卡顿小问题. [bopo]

- - 新版自定义板块操作 - 对应文档更新. [Yi Wang B]

- - 新版自定义板块操作 - 对应文档更新. [Yi Wang B]

- Update commit. [bopo]

- Update commit. [vagrant]

- 更新执行脚本. [bopo]

- Clean code. [vagrant]

- Add requirements.dev. [bopo]

- Clear requirements.txt. [bopo]

- Fix blocknew symbol bug. [bopo]

- 更新测试代码. [bopo]


v0.8.12 (2022-02-09)
--------------------
- Fix blocknew symbol bug. [bopo]


v0.8.11 (2022-02-09)
--------------------
- Fix blocknew symbol bug. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]


v0.8.10 (2022-01-28)
--------------------
- Update holiday. [bopo]

- Update tests. [bopo]


v0.8.9 (2022-01-28)
-------------------
- Fixed makret error. [bopo]

- Fixed makret error. [bopo]


v0.8.8 (2022-01-28)
-------------------
- 解决 logger debug. [bopo]

- 解决北交所股票不能获取数据问题. [bopo]


v0.8.7 (2022-01-28)
-------------------
- 解决北交所股票不能获取数据问题. [bopo]

- 解决北交所股票不能获取数据问题. [bopo]

- Update cli. [bopo]

- Update cli. [bopo]

- Update .pre-commit-config.yaml. [bopo]


v0.8.6 (2022-01-26)
-------------------
- Update holiday. [bopo]


v0.8.5 (2022-01-26)
-------------------
- Update holiday. [bopo]

- Update index, add volume. [bopo]

- Update. [bopo]

- Fix bug. [bopo]

- 修改文档. [bopo]

- 修改文档. [bopo]

- 修改文档. [bopo]

- Update commit. [bopo]


v0.8.4 (2021-12-04)
-------------------
- 修改文档. [bopo]

- 修改接口重试失败后报异常，改为返回为空 df，添加日志静默方式参数. [bopo]

- Format code. [bopo]


v0.8.3 (2021-11-27)
-------------------
- Fix `bestip -v` error bug. [bopo]

- 更新文档. [bopo]


v0.8.2 (2021-10-29)
-------------------
- 修复win下编码问题. [bopo]

- Fixed reader path bug. [bopo]

- Fixed reader path bug. [bopo]

- Fixed reader path bug. [bopo]


v0.8.1 (2021-10-25)
-------------------
- Fixed reader path bug. [bopo]

- Fixed reader path bug. [bopo]


v0.8.0 (2021-10-25)
-------------------
- Update docs. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- Clear code. [bopo]

- Fixed console bug. [bopo]

- Clear logs. [bopo]

- Fix reconnect bug. bestip bug, config bug. [bopo]

- Update commit. [bopo]

- Fix bugs. [bopo]

- Add holiday & factor. [bopo]

- Add holiday & factor. [bopo]

- Update config. [bopo]

- Update config. [bopo]

- Update config. [bopo]

- Update config. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update tdx2csv & test script. [bopo]

- Update changelog. [bopo]

- Update. [bopo]


v0.7.21 (2021-09-24)
--------------------

Fix
~~~
- Config not found. [bopo]


Other
~~~~~
- Update changelog. [bopo]

- Update bestip & test script. [bopo]

- Update commit. [bopo]

- Update docs. [bopo]


v0.7.20 (2021-09-22)
--------------------
- Update docs. [bopo]

- Update affair. [bopo]

- Update affairs. [bopo]

- Clear code . [bopo]

- Clear code . [bopo]

- Update test. [bopo]

- Clear code . [bopo]

- Clear code . [bopo]

- Update fab. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]


v0.7.19 (2021-09-18)
--------------------
- Update docs. [bopo]

- - clear code. - add txt2csv function. [bopo]

- Clear code. [bopo]

- Update. [bopo]

- Update affair. [bopo]

- Update affair. [bopo]

- Update test script. [bopo]

- Update test script. [bopo]

- Update. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- 发布版本. [bopo]

- 发布版本. [bopo]

- Fix bug. [bopo]

- Merge branch 'master' of github.com:mootdx/mootdx. [bopo]


v0.7.18 (2021-09-14)
--------------------

Changes
~~~~~~~
- 修正文档错误. [bopo]

- 修正文档错误. [bopo]


Fix
~~~
- 修改bestip获取错误, 修改整测试脚本错误，修改财务数据下载路径错误. [bopo]

- 修改bestip获取错误 fix: 修改整测试脚本错误 fix: 修改财务数据下载路径错误. [bopo]


Other
~~~~~
- 清理代码. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update changelog. [bopo]


v0.7.17 (2021-09-12)
--------------------

Changes
~~~~~~~
- 财务数据调整为异步下载方式, 性能提升十几倍. [bopo]

- 调整logger, 使用异步方式选择最优服务器ip. [bopo]

- 更新文档. [bopo]


Other
~~~~~
- Pre commit. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- 财务数据调整为异步下载方式, 性能提升十几倍. [bopo]

- 调整logger, 使用异步方式选择最优服务器ip. [bopo]

- Unipath to pathlib. [bopo]

- Unipath to pathlib. [bopo]

- 格式化代码. [bopo]

- 格式化代码. [bopo]

- 项目整理. [bopo]

- Update mootdx/contrib/compat.py. 支持科创版指数基金。 [b0p0m0f0]


v0.7.16 (2021-09-08)
--------------------

Changes
~~~~~~~
- 更新文档. [bopo]


v0.7.15 (2021-09-08)
--------------------

Changes
~~~~~~~
- 更新文档. [bopo]

- 更新文档. [bopo]

- 修复分钟线数据读取bug. [bopo]


Other
~~~~~
- Formant code. [bopo]

- Fix .pre-commit-config.yaml. [bopo]


v0.7.14 (2021-08-24)
--------------------

Fix
~~~
- Update test. [bopo]

- Update test. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]


Other
~~~~~
- Update commit. [bopo]

- Update hotfix. [ibopo]

- Update hotfix. [ibopo]


v0.7.12 (2021-08-04)
--------------------
- Update quotes server. [bopo]

- Update commit. [ibopo]

- Update commit. [ibopo]

- Update commit. [bopo]

- Update docs. [bopo]


v0.7.11 (2021-07-13)
--------------------
- Merge branch 'develop' of gitee.com:ibopo/mootdx into develop. [ibopo]

- !2 bugfix: 查询分笔成交offset不能为market code * bugfix: 查询分笔成交offset不能为market code. [dhrhe]


v0.7.10 (2021-07-05)
--------------------

Changes
~~~~~~~
- Change connecton. [bopo]

- Add log. [bopo]

- Mrage. [bopo]

- Update adjust. [bopo]

- Update to_data. [bopo]

- Update requirements. [bopo]

- Change readme. [bopo]

- Change requirements. [bopo]

- Remove trade server. [bopo]

- Remove trade server. [bopo]


Fix
~~~
- Reader path bug. [bopo]

- 修改. [bopo]

- 修改win下config目录问题. [bopo]

- Update commit. [bopo]


Other
~~~~~
- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update tests. [bopo]

- Update docs. [bopo]

- Clean tests. [bopo]

- Update docs. [bopo]

- Update bestip. [bopo]

- Update import. [bopo]

- Update timeout. [bopo]

- Update bestip. [bopo]

- Update logger. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update block new test. [bopo]

- Update block new test. [bopo]

- Update block new test. [bopo]

- Update test. [bopo]

- Update docs. [bopo]

- Update test. [bopo]

- Update test. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update adjust. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Add: added utils tests. [bopo]

- Bug fix: replace unipath with pathlib. [Bo Zheng]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update reader. [bopo]

- Update reader. [bopo]

- Update transactions. [bopo]

- Update affair. [bopo]

- Update commit. [bopo]

- Update ext market bug. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]


v0.9.11 (2022-12-05)
--------------------
- Fix bugs. [bopo]

- Update docs. [bopo]

- Docs. [bopo]

- 增加复权缓存, 调整依赖版本, 修改若干小问题. [bopo]


v0.9.10 (2022-12-05)
--------------------
- 增加复权缓存, 调整依赖版本. [bopo]


v0.9.9 (2022-11-28)
-------------------
- Fix setup bug. [bopo]


v0.9.8 (2022-11-28)
-------------------
- Fix bugs. [bopo]

- Update comit. [bopo]

- Update comit. [bopo]

- Clear codes. [bopo]

- Clear codes. [bopo]


v0.9.7 (2022-11-24)
-------------------
- Update comit. [bopo]

- Update connect2. [bopo]

- Update makefile. [bopo]

- Added poetry file. [bopo]

- Added poetry file. [bopo]

- Added poetry file. [bopo]


v0.9.6 (2022-11-23)
-------------------
- Update bestip. [bopo]


v0.9.5 (2022-11-23)
-------------------
- Update bestip. [bopo]


v0.9.4 (2022-11-23)
-------------------
- Update bestip. [bopo]

- Update bestip. [bopo]

- Update bestip. [bopo]


v0.9.3 (2022-11-23)
-------------------
- Update commit. [bopo]

- Clear codes. [bopo]

- Clear codes. [bopo]

- Clear tests. [bopo]

- Fixed bugs. [bopo]


v0.9.2 (2022-11-13)
-------------------
- Update setup.cfg. [bopo]

- Update fixtures. [bopo]

- Update logger. [bopo]

- Reader.py 关于通达信特有指数的数据获取修改 #23. [bopo]

- Modify parse. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update commit. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Add readme.md. [bopo]

- Remove loguru. [bopo]

- Remove loguru. [bopo]

- Remove simplejson. [bopo]

- Remove simplejson. [bopo]

- Remove simplejson. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Clean code. [bopo]

- Pytdx -> tdxpy. [bopo]

- Pytdx -> tdxpy. [bopo]

- Update commit. [bopo]

- To_data empty value. [bopo]

- 本地数据日线复权. [bopo]

- 本地数据日线复权. [bopo]

- 本地数据日线复权. [bopo]

- Add: 手动指定市场服务器IP. [bopo]

- Update commit. [bopo]

- Fmt code. [bopo]

- Update makfile. [bopo]

- Update commit. [bopo]

- Update tests. [bopo]

- Fix httpx 0.23. [bopo]

- Add .drone.yml. [bopo]

- Sentry. [bopo]


v0.9.1 (2022-05-14)
-------------------
- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update README.rst. [bopo]

- Update README.rst. [bopo]


v0.9.0 (2022-05-13)
-------------------
- Update README.rst. [bopo]

- Update README.rst. [bopo]

- V0.9.0. [bopo]

  * 自定义板块函数调整, 添加增、删、改、查操作
  * 日志等级调整为自行可配置(之前有反馈说日志等级太低, 太多无用日志，影响性能) 构造函数调整
  * 调整K线数据数据频次参数(frequency)的赋值方式, 原数字方式改成字符, 例如(原15分钟线值`1`改为`15m`)
  * 增加服务器IP功能, 构造函数里添加 `server`参数 例如：`client = Quotes.factory(market='std', server=('127.0.0.0',7727), verbose=0, quiet=True)`
  * 日志过滤的调整
  * 恢复了holiday2
  * 财务数据的表头转为中文, 使用时更加直观
  * 复权算法, 已经修复
- Xdxr 增加当日缓存，加速. [bopo]

- Update todo.md. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- 更block. [bopo]

- 更改json成simplejson. [bopo]

- 更改json成simplejson. [bopo]

- 更新命令行的一个卡顿小问题. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update tests. [bopo]

- √ [文档/测试] 板块读取函数调整, 详情请查看文档 √ [文档] 日志等级调整为自行可配置(之前有反馈说日志等级太低, 太多无用日志，影响性能) 构造函数调整 √ [文档] 调整K线数据数据频次参数(frequency)的赋值方式, 原数字方式改成字符, 例如(原15分钟线值`1`改为`15m`) √ [功能] 增加服务器IP功能, 构造函数里添加 √ [功能] 日志过滤的调整 √ [恢复] 恢复了holiday2 √ [调整] 财务数据的 columns 转中文 √ [调整] 复权算法, 自动结果. [bopo]

- 更新执行脚本. [bopo]

  update commit

  update commit

  - 新版自定义板块操作
  - 对应文档更新

  - 新版自定义板块操作
  - 对应文档更新

  更新命令行的一个卡顿小问题

  更改json成simplejson

  更改json成simplejson

  更block

  Bump version: 0.8.12 → 0.8.13
- Clean code. [bopo]


v0.8.14 (2022-05-08)
--------------------
- Update commit. [bopo]

- - 复权试验. [Yi Wang B]

- Update .readthedocs.yaml. [bopo]

- Update .readthedocs.yaml. [bopo]

- Update .readthedocs.yaml. [bopo]

- Update .readthedocs.yaml. [bopo]


v0.8.13 (2022-05-07)
--------------------
- 更block. [bopo]

- 更改json成simplejson. [bopo]

- 更改json成simplejson. [bopo]

- 更新命令行的一个卡顿小问题. [bopo]

- - 新版自定义板块操作 - 对应文档更新. [Yi Wang B]

- - 新版自定义板块操作 - 对应文档更新. [Yi Wang B]

- Update commit. [bopo]

- Update commit. [vagrant]

- 更新执行脚本. [bopo]

- Clean code. [vagrant]

- Add requirements.dev. [bopo]

- Clear requirements.txt. [bopo]

- Fix blocknew symbol bug. [bopo]

- 更新测试代码. [bopo]


v0.8.12 (2022-02-09)
--------------------
- Fix blocknew symbol bug. [bopo]


v0.8.11 (2022-02-09)
--------------------
- Fix blocknew symbol bug. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]


v0.8.10 (2022-01-28)
--------------------
- Update holiday. [bopo]

- Update tests. [bopo]


v0.8.9 (2022-01-28)
-------------------
- Fixed makret error. [bopo]

- Fixed makret error. [bopo]


v0.8.8 (2022-01-28)
-------------------
- 解决 logger debug. [bopo]

- 解决北交所股票不能获取数据问题. [bopo]


v0.8.7 (2022-01-28)
-------------------
- 解决北交所股票不能获取数据问题. [bopo]

- 解决北交所股票不能获取数据问题. [bopo]

- Update cli. [bopo]

- Update cli. [bopo]

- Update .pre-commit-config.yaml. [bopo]


v0.8.6 (2022-01-26)
-------------------
- Update holiday. [bopo]


v0.8.5 (2022-01-26)
-------------------
- Update holiday. [bopo]

- Update index, add volume. [bopo]

- Update. [bopo]

- Fix bug. [bopo]

- 修改文档. [bopo]

- 修改文档. [bopo]

- 修改文档. [bopo]

- Update commit. [bopo]


v0.8.4 (2021-12-04)
-------------------
- 修改文档. [bopo]

- 修改接口重试失败后报异常，改为返回为空 df，添加日志静默方式参数. [bopo]

- Format code. [bopo]


v0.8.3 (2021-11-27)
-------------------
- Fix `bestip -v` error bug. [bopo]

- 更新文档. [bopo]


v0.8.2 (2021-10-29)
-------------------
- 修复win下编码问题. [bopo]

- Fixed reader path bug. [bopo]

- Fixed reader path bug. [bopo]

- Fixed reader path bug. [bopo]


v0.8.1 (2021-10-25)
-------------------
- Fixed reader path bug. [bopo]

- Fixed reader path bug. [bopo]


v0.8.0 (2021-10-25)
-------------------
- Update docs. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- Clear code. [bopo]

- Fixed console bug. [bopo]

- Clear logs. [bopo]

- Fix reconnect bug. bestip bug, config bug. [bopo]

- Update commit. [bopo]

- Fix bugs. [bopo]

- Add holiday & factor. [bopo]

- Add holiday & factor. [bopo]

- Update config. [bopo]

- Update config. [bopo]

- Update config. [bopo]

- Update config. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update tdx2csv & test script. [bopo]

- Update changelog. [bopo]

- Update. [bopo]


v0.7.21 (2021-09-24)
--------------------

Fix
~~~
- Config not found. [bopo]


Other
~~~~~
- Update changelog. [bopo]

- Update bestip & test script. [bopo]

- Update commit. [bopo]

- Update docs. [bopo]


v0.7.20 (2021-09-22)
--------------------
- Update docs. [bopo]

- Update affair. [bopo]

- Update affairs. [bopo]

- Clear code . [bopo]

- Clear code . [bopo]

- Update test. [bopo]

- Clear code . [bopo]

- Clear code . [bopo]

- Update fab. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]


v0.7.19 (2021-09-18)
--------------------
- Update docs. [bopo]

- - clear code. - add txt2csv function. [bopo]

- Clear code. [bopo]

- Update. [bopo]

- Update affair. [bopo]

- Update affair. [bopo]

- Update test script. [bopo]

- Update test script. [bopo]

- Update. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- 发布版本. [bopo]

- 发布版本. [bopo]

- Fix bug. [bopo]

- Merge branch 'master' of github.com:mootdx/mootdx. [bopo]


v0.7.18 (2021-09-14)
--------------------

Changes
~~~~~~~
- 修正文档错误. [bopo]

- 修正文档错误. [bopo]


Fix
~~~
- 修改bestip获取错误, 修改整测试脚本错误，修改财务数据下载路径错误. [bopo]

- 修改bestip获取错误 fix: 修改整测试脚本错误 fix: 修改财务数据下载路径错误. [bopo]


Other
~~~~~
- 清理代码. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update changelog. [bopo]


v0.7.17 (2021-09-12)
--------------------

Changes
~~~~~~~
- 财务数据调整为异步下载方式, 性能提升十几倍. [bopo]

- 调整logger, 使用异步方式选择最优服务器ip. [bopo]

- 更新文档. [bopo]


Other
~~~~~
- Pre commit. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- 财务数据调整为异步下载方式, 性能提升十几倍. [bopo]

- 调整logger, 使用异步方式选择最优服务器ip. [bopo]

- Unipath to pathlib. [bopo]

- Unipath to pathlib. [bopo]

- 格式化代码. [bopo]

- 格式化代码. [bopo]

- 项目整理. [bopo]

- Update mootdx/contrib/compat.py. 支持科创版指数基金。 [b0p0m0f0]


v0.7.16 (2021-09-08)
--------------------

Changes
~~~~~~~
- 更新文档. [bopo]


v0.7.15 (2021-09-08)
--------------------

Changes
~~~~~~~
- 更新文档. [bopo]

- 更新文档. [bopo]

- 修复分钟线数据读取bug. [bopo]


Other
~~~~~
- Formant code. [bopo]

- Fix .pre-commit-config.yaml. [bopo]


v0.7.14 (2021-08-24)
--------------------

Fix
~~~
- Update test. [bopo]

- Update test. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]


Other
~~~~~
- Update commit. [bopo]

- Update hotfix. [ibopo]

- Update hotfix. [ibopo]


v0.7.12 (2021-08-04)
--------------------
- Update quotes server. [bopo]

- Update commit. [ibopo]

- Update commit. [ibopo]

- Update commit. [bopo]

- Update docs. [bopo]


v0.7.11 (2021-07-13)
--------------------
- Merge branch 'develop' of gitee.com:ibopo/mootdx into develop. [ibopo]

- !2 bugfix: 查询分笔成交offset不能为market code * bugfix: 查询分笔成交offset不能为market code. [dhrhe]


v0.7.10 (2021-07-05)
--------------------

Changes
~~~~~~~
- Change connecton. [bopo]

- Add log. [bopo]

- Mrage. [bopo]

- Update adjust. [bopo]

- Update to_data. [bopo]

- Update requirements. [bopo]

- Change readme. [bopo]

- Change requirements. [bopo]

- Remove trade server. [bopo]

- Remove trade server. [bopo]


Fix
~~~
- Reader path bug. [bopo]

- 修改. [bopo]

- 修改win下config目录问题. [bopo]

- Update commit. [bopo]


Other
~~~~~
- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update tests. [bopo]

- Update docs. [bopo]

- Clean tests. [bopo]

- Update docs. [bopo]

- Update bestip. [bopo]

- Update import. [bopo]

- Update timeout. [bopo]

- Update bestip. [bopo]

- Update logger. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update block new test. [bopo]

- Update block new test. [bopo]

- Update block new test. [bopo]

- Update test. [bopo]

- Update docs. [bopo]

- Update test. [bopo]

- Update test. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update adjust. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Add: added utils tests. [bopo]

- Bug fix: replace unipath with pathlib. [Bo Zheng]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update reader. [bopo]

- Update reader. [bopo]

- Update transactions. [bopo]

- Update affair. [bopo]

- Update commit. [bopo]

- Update ext market bug. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]


v0.9.11 (2022-12-05)
--------------------
- Fix bugs. [bopo]

- Update docs. [bopo]

- Docs. [bopo]

- 增加复权缓存, 调整依赖版本, 修改若干小问题. [bopo]


v0.9.10 (2022-12-05)
--------------------
- 增加复权缓存, 调整依赖版本. [bopo]


v0.9.9 (2022-11-28)
-------------------
- Fix setup bug. [bopo]


v0.9.8 (2022-11-28)
-------------------
- Fix bugs. [bopo]

- Update comit. [bopo]

- Update comit. [bopo]

- Clear codes. [bopo]

- Clear codes. [bopo]


v0.9.7 (2022-11-24)
-------------------
- Update comit. [bopo]

- Update connect2. [bopo]

- Update makefile. [bopo]

- Added poetry file. [bopo]

- Added poetry file. [bopo]

- Added poetry file. [bopo]


v0.9.6 (2022-11-23)
-------------------
- Update bestip. [bopo]


v0.9.5 (2022-11-23)
-------------------
- Update bestip. [bopo]


v0.9.4 (2022-11-23)
-------------------
- Update bestip. [bopo]

- Update bestip. [bopo]

- Update bestip. [bopo]


v0.9.3 (2022-11-23)
-------------------
- Update commit. [bopo]

- Clear codes. [bopo]

- Clear codes. [bopo]

- Clear tests. [bopo]

- Fixed bugs. [bopo]


v0.9.2 (2022-11-13)
-------------------
- Update setup.cfg. [bopo]

- Update fixtures. [bopo]

- Update logger. [bopo]

- Reader.py 关于通达信特有指数的数据获取修改 #23. [bopo]

- Modify parse. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update commit. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Add readme.md. [bopo]

- Remove loguru. [bopo]

- Remove loguru. [bopo]

- Remove simplejson. [bopo]

- Remove simplejson. [bopo]

- Remove simplejson. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Clean code. [bopo]

- Pytdx -> tdxpy. [bopo]

- Pytdx -> tdxpy. [bopo]

- Update commit. [bopo]

- To_data empty value. [bopo]

- 本地数据日线复权. [bopo]

- 本地数据日线复权. [bopo]

- 本地数据日线复权. [bopo]

- Add: 手动指定市场服务器IP. [bopo]

- Update commit. [bopo]

- Fmt code. [bopo]

- Update makfile. [bopo]

- Update commit. [bopo]

- Update tests. [bopo]

- Fix httpx 0.23. [bopo]

- Add .drone.yml. [bopo]

- Sentry. [bopo]


v0.9.1 (2022-05-14)
-------------------
- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update README.rst. [bopo]

- Update README.rst. [bopo]


v0.9.0 (2022-05-13)
-------------------
- Update README.rst. [bopo]

- Update README.rst. [bopo]

- V0.9.0. [bopo]

  * 自定义板块函数调整, 添加增、删、改、查操作
  * 日志等级调整为自行可配置(之前有反馈说日志等级太低, 太多无用日志，影响性能) 构造函数调整
  * 调整K线数据数据频次参数(frequency)的赋值方式, 原数字方式改成字符, 例如(原15分钟线值`1`改为`15m`)
  * 增加服务器IP功能, 构造函数里添加 `server`参数 例如：`client = Quotes.factory(market='std', server=('127.0.0.0',7727), verbose=0, quiet=True)`
  * 日志过滤的调整
  * 恢复了holiday2
  * 财务数据的表头转为中文, 使用时更加直观
  * 复权算法, 已经修复
- Xdxr 增加当日缓存，加速. [bopo]

- Update todo.md. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- 更block. [bopo]

- 更改json成simplejson. [bopo]

- 更改json成simplejson. [bopo]

- 更新命令行的一个卡顿小问题. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update tests. [bopo]

- √ [文档/测试] 板块读取函数调整, 详情请查看文档 √ [文档] 日志等级调整为自行可配置(之前有反馈说日志等级太低, 太多无用日志，影响性能) 构造函数调整 √ [文档] 调整K线数据数据频次参数(frequency)的赋值方式, 原数字方式改成字符, 例如(原15分钟线值`1`改为`15m`) √ [功能] 增加服务器IP功能, 构造函数里添加 √ [功能] 日志过滤的调整 √ [恢复] 恢复了holiday2 √ [调整] 财务数据的 columns 转中文 √ [调整] 复权算法, 自动结果. [bopo]

- 更新执行脚本. [bopo]

  update commit

  update commit

  - 新版自定义板块操作
  - 对应文档更新

  - 新版自定义板块操作
  - 对应文档更新

  更新命令行的一个卡顿小问题

  更改json成simplejson

  更改json成simplejson

  更block

  Bump version: 0.8.12 → 0.8.13
- Clean code. [bopo]


v0.8.14 (2022-05-08)
--------------------
- Update commit. [bopo]

- - 复权试验. [Yi Wang B]

- Update .readthedocs.yaml. [bopo]

- Update .readthedocs.yaml. [bopo]

- Update .readthedocs.yaml. [bopo]

- Update .readthedocs.yaml. [bopo]


v0.8.13 (2022-05-07)
--------------------
- 更block. [bopo]

- 更改json成simplejson. [bopo]

- 更改json成simplejson. [bopo]

- 更新命令行的一个卡顿小问题. [bopo]

- - 新版自定义板块操作 - 对应文档更新. [Yi Wang B]

- - 新版自定义板块操作 - 对应文档更新. [Yi Wang B]

- Update commit. [bopo]

- Update commit. [vagrant]

- 更新执行脚本. [bopo]

- Clean code. [vagrant]

- Add requirements.dev. [bopo]

- Clear requirements.txt. [bopo]

- Fix blocknew symbol bug. [bopo]

- 更新测试代码. [bopo]


v0.8.12 (2022-02-09)
--------------------
- Fix blocknew symbol bug. [bopo]


v0.8.11 (2022-02-09)
--------------------
- Fix blocknew symbol bug. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]


v0.8.10 (2022-01-28)
--------------------
- Update holiday. [bopo]

- Update tests. [bopo]


v0.8.9 (2022-01-28)
-------------------
- Fixed makret error. [bopo]

- Fixed makret error. [bopo]


v0.8.8 (2022-01-28)
-------------------
- 解决 logger debug. [bopo]

- 解决北交所股票不能获取数据问题. [bopo]


v0.8.7 (2022-01-28)
-------------------
- 解决北交所股票不能获取数据问题. [bopo]

- 解决北交所股票不能获取数据问题. [bopo]

- Update cli. [bopo]

- Update cli. [bopo]

- Update .pre-commit-config.yaml. [bopo]


v0.8.6 (2022-01-26)
-------------------
- Update holiday. [bopo]


v0.8.5 (2022-01-26)
-------------------
- Update holiday. [bopo]

- Update index, add volume. [bopo]

- Update. [bopo]

- Fix bug. [bopo]

- 修改文档. [bopo]

- 修改文档. [bopo]

- 修改文档. [bopo]

- Update commit. [bopo]


v0.8.4 (2021-12-04)
-------------------
- 修改文档. [bopo]

- 修改接口重试失败后报异常，改为返回为空 df，添加日志静默方式参数. [bopo]

- Format code. [bopo]


v0.8.3 (2021-11-27)
-------------------
- Fix `bestip -v` error bug. [bopo]

- 更新文档. [bopo]


v0.8.2 (2021-10-29)
-------------------
- 修复win下编码问题. [bopo]

- Fixed reader path bug. [bopo]

- Fixed reader path bug. [bopo]

- Fixed reader path bug. [bopo]


v0.8.1 (2021-10-25)
-------------------
- Fixed reader path bug. [bopo]

- Fixed reader path bug. [bopo]


v0.8.0 (2021-10-25)
-------------------
- Update docs. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- Clear code. [bopo]

- Fixed console bug. [bopo]

- Clear logs. [bopo]

- Fix reconnect bug. bestip bug, config bug. [bopo]

- Update commit. [bopo]

- Fix bugs. [bopo]

- Add holiday & factor. [bopo]

- Add holiday & factor. [bopo]

- Update config. [bopo]

- Update config. [bopo]

- Update config. [bopo]

- Update config. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update tdx2csv & test script. [bopo]

- Update changelog. [bopo]

- Update. [bopo]


v0.7.21 (2021-09-24)
--------------------

Fix
~~~
- Config not found. [bopo]


Other
~~~~~
- Update changelog. [bopo]

- Update bestip & test script. [bopo]

- Update commit. [bopo]

- Update docs. [bopo]


v0.7.20 (2021-09-22)
--------------------
- Update docs. [bopo]

- Update affair. [bopo]

- Update affairs. [bopo]

- Clear code . [bopo]

- Clear code . [bopo]

- Update test. [bopo]

- Clear code . [bopo]

- Clear code . [bopo]

- Update fab. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]


v0.7.19 (2021-09-18)
--------------------
- Update docs. [bopo]

- - clear code. - add txt2csv function. [bopo]

- Clear code. [bopo]

- Update. [bopo]

- Update affair. [bopo]

- Update affair. [bopo]

- Update test script. [bopo]

- Update test script. [bopo]

- Update. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- 发布版本. [bopo]

- 发布版本. [bopo]

- Fix bug. [bopo]

- Merge branch 'master' of github.com:mootdx/mootdx. [bopo]


v0.7.18 (2021-09-14)
--------------------

Changes
~~~~~~~
- 修正文档错误. [bopo]

- 修正文档错误. [bopo]


Fix
~~~
- 修改bestip获取错误, 修改整测试脚本错误，修改财务数据下载路径错误. [bopo]

- 修改bestip获取错误 fix: 修改整测试脚本错误 fix: 修改财务数据下载路径错误. [bopo]


Other
~~~~~
- 清理代码. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update changelog. [bopo]


v0.7.17 (2021-09-12)
--------------------

Changes
~~~~~~~
- 财务数据调整为异步下载方式, 性能提升十几倍. [bopo]

- 调整logger, 使用异步方式选择最优服务器ip. [bopo]

- 更新文档. [bopo]


Other
~~~~~
- Pre commit. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- 财务数据调整为异步下载方式, 性能提升十几倍. [bopo]

- 调整logger, 使用异步方式选择最优服务器ip. [bopo]

- Unipath to pathlib. [bopo]

- Unipath to pathlib. [bopo]

- 格式化代码. [bopo]

- 格式化代码. [bopo]

- 项目整理. [bopo]

- Update mootdx/contrib/compat.py. 支持科创版指数基金。 [b0p0m0f0]


v0.7.16 (2021-09-08)
--------------------

Changes
~~~~~~~
- 更新文档. [bopo]


v0.7.15 (2021-09-08)
--------------------

Changes
~~~~~~~
- 更新文档. [bopo]

- 更新文档. [bopo]

- 修复分钟线数据读取bug. [bopo]


Other
~~~~~
- Formant code. [bopo]

- Fix .pre-commit-config.yaml. [bopo]


v0.7.14 (2021-08-24)
--------------------

Fix
~~~
- Update test. [bopo]

- Update test. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]


Other
~~~~~
- Update commit. [bopo]

- Update hotfix. [ibopo]

- Update hotfix. [ibopo]


v0.7.12 (2021-08-04)
--------------------
- Update quotes server. [bopo]

- Update commit. [ibopo]

- Update commit. [ibopo]

- Update commit. [bopo]

- Update docs. [bopo]


v0.7.11 (2021-07-13)
--------------------
- Merge branch 'develop' of gitee.com:ibopo/mootdx into develop. [ibopo]

- !2 bugfix: 查询分笔成交offset不能为market code * bugfix: 查询分笔成交offset不能为market code. [dhrhe]


v0.7.10 (2021-07-05)
--------------------

Changes
~~~~~~~
- Change connecton. [bopo]

- Add log. [bopo]

- Mrage. [bopo]

- Update adjust. [bopo]

- Update to_data. [bopo]

- Update requirements. [bopo]

- Change readme. [bopo]

- Change requirements. [bopo]

- Remove trade server. [bopo]

- Remove trade server. [bopo]


Fix
~~~
- Reader path bug. [bopo]

- 修改. [bopo]

- 修改win下config目录问题. [bopo]

- Update commit. [bopo]


Other
~~~~~
- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update tests. [bopo]

- Update docs. [bopo]

- Clean tests. [bopo]

- Update docs. [bopo]

- Update bestip. [bopo]

- Update import. [bopo]

- Update timeout. [bopo]

- Update bestip. [bopo]

- Update logger. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update block new test. [bopo]

- Update block new test. [bopo]

- Update block new test. [bopo]

- Update test. [bopo]

- Update docs. [bopo]

- Update test. [bopo]

- Update test. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update adjust. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Add: added utils tests. [bopo]

- Bug fix: replace unipath with pathlib. [Bo Zheng]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update reader. [bopo]

- Update reader. [bopo]

- Update transactions. [bopo]

- Update affair. [bopo]

- Update commit. [bopo]

- Update ext market bug. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]


v0.9.11 (2022-12-05)
--------------------
- Fix bugs. [bopo]

- Update docs. [bopo]

- Docs. [bopo]

- 增加复权缓存, 调整依赖版本, 修改若干小问题. [bopo]


v0.9.10 (2022-12-05)
--------------------
- 增加复权缓存, 调整依赖版本. [bopo]


v0.9.9 (2022-11-28)
-------------------
- Fix setup bug. [bopo]


v0.9.8 (2022-11-28)
-------------------
- Fix bugs. [bopo]

- Update comit. [bopo]

- Update comit. [bopo]

- Clear codes. [bopo]

- Clear codes. [bopo]


v0.9.7 (2022-11-24)
-------------------
- Update comit. [bopo]

- Update connect2. [bopo]

- Update makefile. [bopo]

- Added poetry file. [bopo]

- Added poetry file. [bopo]

- Added poetry file. [bopo]


v0.9.6 (2022-11-23)
-------------------
- Update bestip. [bopo]


v0.9.5 (2022-11-23)
-------------------
- Update bestip. [bopo]


v0.9.4 (2022-11-23)
-------------------
- Update bestip. [bopo]

- Update bestip. [bopo]

- Update bestip. [bopo]


v0.9.3 (2022-11-23)
-------------------
- Update commit. [bopo]

- Clear codes. [bopo]

- Clear codes. [bopo]

- Clear tests. [bopo]

- Fixed bugs. [bopo]


v0.9.2 (2022-11-13)
-------------------
- Update setup.cfg. [bopo]

- Update fixtures. [bopo]

- Update logger. [bopo]

- Reader.py 关于通达信特有指数的数据获取修改 #23. [bopo]

- Modify parse. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update commit. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Add readme.md. [bopo]

- Remove loguru. [bopo]

- Remove loguru. [bopo]

- Remove simplejson. [bopo]

- Remove simplejson. [bopo]

- Remove simplejson. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Clean code. [bopo]

- Pytdx -> tdxpy. [bopo]

- Pytdx -> tdxpy. [bopo]

- Update commit. [bopo]

- To_data empty value. [bopo]

- 本地数据日线复权. [bopo]

- 本地数据日线复权. [bopo]

- 本地数据日线复权. [bopo]

- Add: 手动指定市场服务器IP. [bopo]

- Update commit. [bopo]

- Fmt code. [bopo]

- Update makfile. [bopo]

- Update commit. [bopo]

- Update tests. [bopo]

- Fix httpx 0.23. [bopo]

- Add .drone.yml. [bopo]

- Sentry. [bopo]


v0.9.1 (2022-05-14)
-------------------
- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update README.rst. [bopo]

- Update README.rst. [bopo]


v0.9.0 (2022-05-13)
-------------------
- Update README.rst. [bopo]

- Update README.rst. [bopo]

- V0.9.0. [bopo]

  * 自定义板块函数调整, 添加增、删、改、查操作
  * 日志等级调整为自行可配置(之前有反馈说日志等级太低, 太多无用日志，影响性能) 构造函数调整
  * 调整K线数据数据频次参数(frequency)的赋值方式, 原数字方式改成字符, 例如(原15分钟线值`1`改为`15m`)
  * 增加服务器IP功能, 构造函数里添加 `server`参数 例如：`client = Quotes.factory(market='std', server=('127.0.0.0',7727), verbose=0, quiet=True)`
  * 日志过滤的调整
  * 恢复了holiday2
  * 财务数据的表头转为中文, 使用时更加直观
  * 复权算法, 已经修复
- Xdxr 增加当日缓存，加速. [bopo]

- Update todo.md. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- 更block. [bopo]

- 更改json成simplejson. [bopo]

- 更改json成simplejson. [bopo]

- 更新命令行的一个卡顿小问题. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update tests. [bopo]

- √ [文档/测试] 板块读取函数调整, 详情请查看文档 √ [文档] 日志等级调整为自行可配置(之前有反馈说日志等级太低, 太多无用日志，影响性能) 构造函数调整 √ [文档] 调整K线数据数据频次参数(frequency)的赋值方式, 原数字方式改成字符, 例如(原15分钟线值`1`改为`15m`) √ [功能] 增加服务器IP功能, 构造函数里添加 √ [功能] 日志过滤的调整 √ [恢复] 恢复了holiday2 √ [调整] 财务数据的 columns 转中文 √ [调整] 复权算法, 自动结果. [bopo]

- 更新执行脚本. [bopo]

  update commit

  update commit

  - 新版自定义板块操作
  - 对应文档更新

  - 新版自定义板块操作
  - 对应文档更新

  更新命令行的一个卡顿小问题

  更改json成simplejson

  更改json成simplejson

  更block

  Bump version: 0.8.12 → 0.8.13
- Clean code. [bopo]


v0.8.14 (2022-05-08)
--------------------
- Update commit. [bopo]

- - 复权试验. [Yi Wang B]

- Update .readthedocs.yaml. [bopo]

- Update .readthedocs.yaml. [bopo]

- Update .readthedocs.yaml. [bopo]

- Update .readthedocs.yaml. [bopo]


v0.8.13 (2022-05-07)
--------------------
- 更block. [bopo]

- 更改json成simplejson. [bopo]

- 更改json成simplejson. [bopo]

- 更新命令行的一个卡顿小问题. [bopo]

- - 新版自定义板块操作 - 对应文档更新. [Yi Wang B]

- - 新版自定义板块操作 - 对应文档更新. [Yi Wang B]

- Update commit. [bopo]

- Update commit. [vagrant]

- 更新执行脚本. [bopo]

- Clean code. [vagrant]

- Add requirements.dev. [bopo]

- Clear requirements.txt. [bopo]

- Fix blocknew symbol bug. [bopo]

- 更新测试代码. [bopo]


v0.8.12 (2022-02-09)
--------------------
- Fix blocknew symbol bug. [bopo]


v0.8.11 (2022-02-09)
--------------------
- Fix blocknew symbol bug. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]


v0.8.10 (2022-01-28)
--------------------
- Update holiday. [bopo]

- Update tests. [bopo]


v0.8.9 (2022-01-28)
-------------------
- Fixed makret error. [bopo]

- Fixed makret error. [bopo]


v0.8.8 (2022-01-28)
-------------------
- 解决 logger debug. [bopo]

- 解决北交所股票不能获取数据问题. [bopo]


v0.8.7 (2022-01-28)
-------------------
- 解决北交所股票不能获取数据问题. [bopo]

- 解决北交所股票不能获取数据问题. [bopo]

- Update cli. [bopo]

- Update cli. [bopo]

- Update .pre-commit-config.yaml. [bopo]


v0.8.6 (2022-01-26)
-------------------
- Update holiday. [bopo]


v0.8.5 (2022-01-26)
-------------------
- Update holiday. [bopo]

- Update index, add volume. [bopo]

- Update. [bopo]

- Fix bug. [bopo]

- 修改文档. [bopo]

- 修改文档. [bopo]

- 修改文档. [bopo]

- Update commit. [bopo]


v0.8.4 (2021-12-04)
-------------------
- 修改文档. [bopo]

- 修改接口重试失败后报异常，改为返回为空 df，添加日志静默方式参数. [bopo]

- Format code. [bopo]


v0.8.3 (2021-11-27)
-------------------
- Fix `bestip -v` error bug. [bopo]

- 更新文档. [bopo]


v0.8.2 (2021-10-29)
-------------------
- 修复win下编码问题. [bopo]

- Fixed reader path bug. [bopo]

- Fixed reader path bug. [bopo]

- Fixed reader path bug. [bopo]


v0.8.1 (2021-10-25)
-------------------
- Fixed reader path bug. [bopo]

- Fixed reader path bug. [bopo]


v0.8.0 (2021-10-25)
-------------------
- Update docs. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- Clear code. [bopo]

- Fixed console bug. [bopo]

- Clear logs. [bopo]

- Fix reconnect bug. bestip bug, config bug. [bopo]

- Update commit. [bopo]

- Fix bugs. [bopo]

- Add holiday & factor. [bopo]

- Add holiday & factor. [bopo]

- Update config. [bopo]

- Update config. [bopo]

- Update config. [bopo]

- Update config. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update tdx2csv & test script. [bopo]

- Update changelog. [bopo]

- Update. [bopo]


v0.7.21 (2021-09-24)
--------------------

Fix
~~~
- Config not found. [bopo]


Other
~~~~~
- Update changelog. [bopo]

- Update bestip & test script. [bopo]

- Update commit. [bopo]

- Update docs. [bopo]


v0.7.20 (2021-09-22)
--------------------
- Update docs. [bopo]

- Update affair. [bopo]

- Update affairs. [bopo]

- Clear code . [bopo]

- Clear code . [bopo]

- Update test. [bopo]

- Clear code . [bopo]

- Clear code . [bopo]

- Update fab. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]


v0.7.19 (2021-09-18)
--------------------
- Update docs. [bopo]

- - clear code. - add txt2csv function. [bopo]

- Clear code. [bopo]

- Update. [bopo]

- Update affair. [bopo]

- Update affair. [bopo]

- Update test script. [bopo]

- Update test script. [bopo]

- Update. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- 发布版本. [bopo]

- 发布版本. [bopo]

- Fix bug. [bopo]

- Merge branch 'master' of github.com:mootdx/mootdx. [bopo]


v0.7.18 (2021-09-14)
--------------------

Changes
~~~~~~~
- 修正文档错误. [bopo]

- 修正文档错误. [bopo]


Fix
~~~
- 修改bestip获取错误, 修改整测试脚本错误，修改财务数据下载路径错误. [bopo]

- 修改bestip获取错误 fix: 修改整测试脚本错误 fix: 修改财务数据下载路径错误. [bopo]


Other
~~~~~
- 清理代码. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update changelog. [bopo]


v0.7.17 (2021-09-12)
--------------------

Changes
~~~~~~~
- 财务数据调整为异步下载方式, 性能提升十几倍. [bopo]

- 调整logger, 使用异步方式选择最优服务器ip. [bopo]

- 更新文档. [bopo]


Other
~~~~~
- Pre commit. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- 财务数据调整为异步下载方式, 性能提升十几倍. [bopo]

- 调整logger, 使用异步方式选择最优服务器ip. [bopo]

- Unipath to pathlib. [bopo]

- Unipath to pathlib. [bopo]

- 格式化代码. [bopo]

- 格式化代码. [bopo]

- 项目整理. [bopo]

- Update mootdx/contrib/compat.py. 支持科创版指数基金。 [b0p0m0f0]


v0.7.16 (2021-09-08)
--------------------

Changes
~~~~~~~
- 更新文档. [bopo]


v0.7.15 (2021-09-08)
--------------------

Changes
~~~~~~~
- 更新文档. [bopo]

- 更新文档. [bopo]

- 修复分钟线数据读取bug. [bopo]


Other
~~~~~
- Formant code. [bopo]

- Fix .pre-commit-config.yaml. [bopo]


v0.7.14 (2021-08-24)
--------------------

Fix
~~~
- Update test. [bopo]

- Update test. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]


Other
~~~~~
- Update commit. [bopo]

- Update hotfix. [ibopo]

- Update hotfix. [ibopo]


v0.7.12 (2021-08-04)
--------------------
- Update quotes server. [bopo]

- Update commit. [ibopo]

- Update commit. [ibopo]

- Update commit. [bopo]

- Update docs. [bopo]


v0.7.11 (2021-07-13)
--------------------
- Merge branch 'develop' of gitee.com:ibopo/mootdx into develop. [ibopo]

- !2 bugfix: 查询分笔成交offset不能为market code * bugfix: 查询分笔成交offset不能为market code. [dhrhe]


v0.7.10 (2021-07-05)
--------------------

Changes
~~~~~~~
- Change connecton. [bopo]

- Add log. [bopo]

- Mrage. [bopo]

- Update adjust. [bopo]

- Update to_data. [bopo]

- Update requirements. [bopo]

- Change readme. [bopo]

- Change requirements. [bopo]

- Remove trade server. [bopo]

- Remove trade server. [bopo]


Fix
~~~
- Reader path bug. [bopo]

- 修改. [bopo]

- 修改win下config目录问题. [bopo]

- Update commit. [bopo]


Other
~~~~~
- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update tests. [bopo]

- Update docs. [bopo]

- Clean tests. [bopo]

- Update docs. [bopo]

- Update bestip. [bopo]

- Update import. [bopo]

- Update timeout. [bopo]

- Update bestip. [bopo]

- Update logger. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update block new test. [bopo]

- Update block new test. [bopo]

- Update block new test. [bopo]

- Update test. [bopo]

- Update docs. [bopo]

- Update test. [bopo]

- Update test. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update adjust. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Add: added utils tests. [bopo]

- Bug fix: replace unipath with pathlib. [Bo Zheng]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update reader. [bopo]

- Update reader. [bopo]

- Update transactions. [bopo]

- Update affair. [bopo]

- Update commit. [bopo]

- Update ext market bug. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]


v0.9.8 (2022-11-28)
-------------------
- Fix bugs. [bopo]

- Update comit. [bopo]

- Update comit. [bopo]

- Clear codes. [bopo]

- Clear codes. [bopo]


v0.9.7 (2022-11-24)
-------------------
- Update comit. [bopo]

- Update connect2. [bopo]

- Update makefile. [bopo]

- Added poetry file. [bopo]

- Added poetry file. [bopo]

- Added poetry file. [bopo]


v0.9.6 (2022-11-23)
-------------------
- Update bestip. [bopo]


v0.9.5 (2022-11-23)
-------------------
- Update bestip. [bopo]


v0.9.4 (2022-11-23)
-------------------
- Update bestip. [bopo]

- Update bestip. [bopo]

- Update bestip. [bopo]


v0.9.3 (2022-11-23)
-------------------
- Update commit. [bopo]

- Clear codes. [bopo]

- Clear codes. [bopo]

- Clear tests. [bopo]

- Fixed bugs. [bopo]


v0.9.2 (2022-11-13)
-------------------
- Update setup.cfg. [bopo]

- Update fixtures. [bopo]

- Update logger. [bopo]

- Reader.py 关于通达信特有指数的数据获取修改 #23. [bopo]

- Modify parse. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update commit. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Modify drone.yaml. [bopo]

- Add readme.md. [bopo]

- Remove loguru. [bopo]

- Remove loguru. [bopo]

- Remove simplejson. [bopo]

- Remove simplejson. [bopo]

- Remove simplejson. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Clean code. [bopo]

- Pytdx -> tdxpy. [bopo]

- Pytdx -> tdxpy. [bopo]

- Update commit. [bopo]

- To_data empty value. [bopo]

- 本地数据日线复权. [bopo]

- 本地数据日线复权. [bopo]

- 本地数据日线复权. [bopo]

- Add: 手动指定市场服务器IP. [bopo]

- Update commit. [bopo]

- Fmt code. [bopo]

- Update makfile. [bopo]

- Update commit. [bopo]

- Update tests. [bopo]

- Fix httpx 0.23. [bopo]

- Add .drone.yml. [bopo]

- Sentry. [bopo]


v0.9.1 (2022-05-14)
-------------------
- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update README.rst. [bopo]

- Update README.rst. [bopo]


v0.9.0 (2022-05-13)
-------------------
- Update README.rst. [bopo]

- Update README.rst. [bopo]

- V0.9.0. [bopo]

  * 自定义板块函数调整, 添加增、删、改、查操作
  * 日志等级调整为自行可配置(之前有反馈说日志等级太低, 太多无用日志，影响性能) 构造函数调整
  * 调整K线数据数据频次参数(frequency)的赋值方式, 原数字方式改成字符, 例如(原15分钟线值`1`改为`15m`)
  * 增加服务器IP功能, 构造函数里添加 `server`参数 例如：`client = Quotes.factory(market='std', server=('127.0.0.0',7727), verbose=0, quiet=True)`
  * 日志过滤的调整
  * 恢复了holiday2
  * 财务数据的表头转为中文, 使用时更加直观
  * 复权算法, 已经修复
- Xdxr 增加当日缓存，加速. [bopo]

- Update todo.md. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- 更block. [bopo]

- 更改json成simplejson. [bopo]

- 更改json成simplejson. [bopo]

- 更新命令行的一个卡顿小问题. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update tests. [bopo]

- √ [文档/测试] 板块读取函数调整, 详情请查看文档 √ [文档] 日志等级调整为自行可配置(之前有反馈说日志等级太低, 太多无用日志，影响性能) 构造函数调整 √ [文档] 调整K线数据数据频次参数(frequency)的赋值方式, 原数字方式改成字符, 例如(原15分钟线值`1`改为`15m`) √ [功能] 增加服务器IP功能, 构造函数里添加 √ [功能] 日志过滤的调整 √ [恢复] 恢复了holiday2 √ [调整] 财务数据的 columns 转中文 √ [调整] 复权算法, 自动结果. [bopo]

- 更新执行脚本. [bopo]

  update commit

  update commit

  - 新版自定义板块操作
  - 对应文档更新

  - 新版自定义板块操作
  - 对应文档更新

  更新命令行的一个卡顿小问题

  更改json成simplejson

  更改json成simplejson

  更block

  Bump version: 0.8.12 → 0.8.13
- Clean code. [bopo]


v0.8.14 (2022-05-08)
--------------------
- Update commit. [bopo]

- - 复权试验. [Yi Wang B]

- Update .readthedocs.yaml. [bopo]

- Update .readthedocs.yaml. [bopo]

- Update .readthedocs.yaml. [bopo]

- Update .readthedocs.yaml. [bopo]


v0.8.13 (2022-05-07)
--------------------
- 更block. [bopo]

- 更改json成simplejson. [bopo]

- 更改json成simplejson. [bopo]

- 更新命令行的一个卡顿小问题. [bopo]

- - 新版自定义板块操作 - 对应文档更新. [Yi Wang B]

- - 新版自定义板块操作 - 对应文档更新. [Yi Wang B]

- Update commit. [bopo]

- Update commit. [vagrant]

- 更新执行脚本. [bopo]

- Clean code. [vagrant]

- Add requirements.dev. [bopo]

- Clear requirements.txt. [bopo]

- Fix blocknew symbol bug. [bopo]

- 更新测试代码. [bopo]


v0.8.12 (2022-02-09)
--------------------
- Fix blocknew symbol bug. [bopo]


v0.8.11 (2022-02-09)
--------------------
- Fix blocknew symbol bug. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]


v0.8.10 (2022-01-28)
--------------------
- Update holiday. [bopo]

- Update tests. [bopo]


v0.8.9 (2022-01-28)
-------------------
- Fixed makret error. [bopo]

- Fixed makret error. [bopo]


v0.8.8 (2022-01-28)
-------------------
- 解决 logger debug. [bopo]

- 解决北交所股票不能获取数据问题. [bopo]


v0.8.7 (2022-01-28)
-------------------
- 解决北交所股票不能获取数据问题. [bopo]

- 解决北交所股票不能获取数据问题. [bopo]

- Update cli. [bopo]

- Update cli. [bopo]

- Update .pre-commit-config.yaml. [bopo]


v0.8.6 (2022-01-26)
-------------------
- Update holiday. [bopo]


v0.8.5 (2022-01-26)
-------------------
- Update holiday. [bopo]

- Update index, add volume. [bopo]

- Update. [bopo]

- Fix bug. [bopo]

- 修改文档. [bopo]

- 修改文档. [bopo]

- 修改文档. [bopo]

- Update commit. [bopo]


v0.8.4 (2021-12-04)
-------------------
- 修改文档. [bopo]

- 修改接口重试失败后报异常，改为返回为空 df，添加日志静默方式参数. [bopo]

- Format code. [bopo]


v0.8.3 (2021-11-27)
-------------------
- Fix `bestip -v` error bug. [bopo]

- 更新文档. [bopo]


v0.8.2 (2021-10-29)
-------------------
- 修复win下编码问题. [bopo]

- Fixed reader path bug. [bopo]

- Fixed reader path bug. [bopo]

- Fixed reader path bug. [bopo]


v0.8.1 (2021-10-25)
-------------------
- Fixed reader path bug. [bopo]

- Fixed reader path bug. [bopo]


v0.8.0 (2021-10-25)
-------------------
- Update docs. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- Clear code. [bopo]

- Fixed console bug. [bopo]

- Clear logs. [bopo]

- Fix reconnect bug. bestip bug, config bug. [bopo]

- Update commit. [bopo]

- Fix bugs. [bopo]

- Add holiday & factor. [bopo]

- Add holiday & factor. [bopo]

- Update config. [bopo]

- Update config. [bopo]

- Update config. [bopo]

- Update config. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update tdx2csv & test script. [bopo]

- Update changelog. [bopo]

- Update. [bopo]


v0.7.21 (2021-09-24)
--------------------

Fix
~~~
- Config not found. [bopo]


Other
~~~~~
- Update changelog. [bopo]

- Update bestip & test script. [bopo]

- Update commit. [bopo]

- Update docs. [bopo]


v0.7.20 (2021-09-22)
--------------------
- Update docs. [bopo]

- Update affair. [bopo]

- Update affairs. [bopo]

- Clear code . [bopo]

- Clear code . [bopo]

- Update test. [bopo]

- Clear code . [bopo]

- Clear code . [bopo]

- Update fab. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]


v0.7.19 (2021-09-18)
--------------------
- Update docs. [bopo]

- - clear code. - add txt2csv function. [bopo]

- Clear code. [bopo]

- Update. [bopo]

- Update affair. [bopo]

- Update affair. [bopo]

- Update test script. [bopo]

- Update test script. [bopo]

- Update. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- 发布版本. [bopo]

- 发布版本. [bopo]

- Fix bug. [bopo]

- Merge branch 'master' of github.com:mootdx/mootdx. [bopo]


v0.7.18 (2021-09-14)
--------------------

Changes
~~~~~~~
- 修正文档错误. [bopo]

- 修正文档错误. [bopo]


Fix
~~~
- 修改bestip获取错误, 修改整测试脚本错误，修改财务数据下载路径错误. [bopo]

- 修改bestip获取错误 fix: 修改整测试脚本错误 fix: 修改财务数据下载路径错误. [bopo]


Other
~~~~~
- 清理代码. [bopo]

- Update readme. [bopo]

- Update readme. [bopo]

- Update changelog. [bopo]


v0.7.17 (2021-09-12)
--------------------

Changes
~~~~~~~
- 财务数据调整为异步下载方式, 性能提升十几倍. [bopo]

- 调整logger, 使用异步方式选择最优服务器ip. [bopo]

- 更新文档. [bopo]


Other
~~~~~
- Pre commit. [bopo]

- Update docs. [bopo]

- Update docs. [bopo]

- 财务数据调整为异步下载方式, 性能提升十几倍. [bopo]

- 调整logger, 使用异步方式选择最优服务器ip. [bopo]

- Unipath to pathlib. [bopo]

- Unipath to pathlib. [bopo]

- 格式化代码. [bopo]

- 格式化代码. [bopo]

- 项目整理. [bopo]

- Update mootdx/contrib/compat.py. 支持科创版指数基金。 [b0p0m0f0]


v0.7.16 (2021-09-08)
--------------------

Changes
~~~~~~~
- 更新文档. [bopo]


v0.7.15 (2021-09-08)
--------------------

Changes
~~~~~~~
- 更新文档. [bopo]

- 更新文档. [bopo]

- 修复分钟线数据读取bug. [bopo]


Other
~~~~~
- Formant code. [bopo]

- Fix .pre-commit-config.yaml. [bopo]


v0.7.14 (2021-08-24)
--------------------

Fix
~~~
- Update test. [bopo]

- Update test. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]


Other
~~~~~
- Update commit. [bopo]

- Update hotfix. [ibopo]

- Update hotfix. [ibopo]


v0.7.12 (2021-08-04)
--------------------
- Update quotes server. [bopo]

- Update commit. [ibopo]

- Update commit. [ibopo]

- Update commit. [bopo]

- Update docs. [bopo]


v0.7.11 (2021-07-13)
--------------------
- Merge branch 'develop' of gitee.com:ibopo/mootdx into develop. [ibopo]

- !2 bugfix: 查询分笔成交offset不能为market code * bugfix: 查询分笔成交offset不能为market code. [dhrhe]


v0.7.10 (2021-07-05)
--------------------

Changes
~~~~~~~
- Change connecton. [bopo]

- Add log. [bopo]

- Mrage. [bopo]

- Update adjust. [bopo]

- Update to_data. [bopo]

- Update requirements. [bopo]

- Change readme. [bopo]

- Change requirements. [bopo]

- Remove trade server. [bopo]

- Remove trade server. [bopo]


Fix
~~~
- Reader path bug. [bopo]

- 修改. [bopo]

- 修改win下config目录问题. [bopo]

- Update commit. [bopo]


Other
~~~~~
- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update tests. [bopo]

- Update docs. [bopo]

- Clean tests. [bopo]

- Update docs. [bopo]

- Update bestip. [bopo]

- Update import. [bopo]

- Update timeout. [bopo]

- Update bestip. [bopo]

- Update logger. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update block new test. [bopo]

- Update block new test. [bopo]

- Update block new test. [bopo]

- Update test. [bopo]

- Update docs. [bopo]

- Update test. [bopo]

- Update test. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update adjust. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Add: added utils tests. [bopo]

- Bug fix: replace unipath with pathlib. [Bo Zheng]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update reader. [bopo]

- Update reader. [bopo]

- Update transactions. [bopo]

- Update affair. [bopo]

- Update commit. [bopo]

- Update ext market bug. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]

- Update commit. [bopo]


v0.9.11 (2022-12-05)
--------------------
- Fix bugs. [bopo]

- Update docs. [bopo]

- Docs. [bopo]

- 增加复权缓存, 调整依赖版本, 修改若干小问题. [bopo]


v0.9.10 (2022-12-05)
--------------------
- 增加复权缓存, 调整依赖版本. [bopo]


v0.9.9 (2022-11-28)
-------------------
- 修改若干bug. [bopo]


v0.9.8 (2022-11-28)
-------------------
- Fix bugs. [bopo]

- Update comit. [bopo]

- Update comit. [bopo]

- Clear codes. [bopo]

- Clear codes. [bopo]


v0.9.7 (2022-11-24)
-------------------
- Update comit. [bopo]

- Update connect2. [bopo]

- Update makefile. [bopo]

- Added poetry file. [bopo]

- Added poetry file. [bopo]

- Added poetry file. [bopo]


v0.9.6 (2022-11-23)
-------------------
- Update bestip. [bopo]


v0.9.5 (2022-11-23)
-------------------
- Update bestip. [bopo]


v0.9.4 (2022-11-23)
-------------------
- Update bestip.

- Update bestip.

- Update bestip.


v0.9.3 (2022-11-23)
-------------------
- Update commit.

- Clear codes.

- Clear codes.

- Clear tests.

- Fixed bugs.


v0.9.2 (2022-11-13)
-------------------
- Update setup.cfg.

- Update fixtures.

- Update logger.

- Reader.py 关于通达信特有指数的数据获取修改 #23.

- Modify parse.

- Modify drone.yaml.

- Modify drone.yaml.

- Update readme.

- Update readme.

- Update readme.

- Update readme.

- Update readme.

- Update readme.

- Update commit.

- Modify drone.yaml.

- Modify drone.yaml.

- Modify drone.yaml.

- Modify drone.yaml.

- Modify drone.yaml.

- Modify drone.yaml.

- Modify drone.yaml.

- Modify drone.yaml.

- Modify drone.yaml.

- Modify drone.yaml.

- Modify drone.yaml.

- Add readme.md.

- Remove loguru.

- Remove loguru.

- Remove simplejson.

- Remove simplejson.

- Remove simplejson.

- Update commit.

- Update commit.

- Update commit.

- Clean code.

- Pytdx -> tdxpy.

- Pytdx -> tdxpy.

- Update commit.

- To_data empty value.

- 本地数据日线复权.

- 本地数据日线复权.

- 本地数据日线复权.

- Add: 手动指定市场服务器IP.

- Update commit.

- Fmt code.

- Update makfile.

- Update commit.

- Update tests.

- Fix httpx 0.23.

- Add .drone.yml.

- Sentry.


v0.9.1 (2022-05-14)
-------------------
- Udate cmmit. []

- Udate cmmit. []

- Udate cmmit. []

- Udate README.rst. []

- Udate README.rst. []


