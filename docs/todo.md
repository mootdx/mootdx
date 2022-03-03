
## v0.9.0 (2021-01-28)

* [测试]修正扩展市场离线数据读取问题
* [文档+测试]板块读取函数调整, 详情请查看文档
[x] [文档]日志等级调整为自行可配置(之前有反馈说日志等级太低, 太多无用日志，影响性能)
* [文档+测试]调整K线数据数据频次参数(frequency)的赋值方式, 原数字方式改成字符, 例如(原15分钟线值`1`改为`15m`)
* [文档+测试]扩展市场行情服务器`IP`更新
* [文档+测试]复权因子的合并, 目前使用第三方数据
* 文档机构的重写调整

```python
from mootdx import logger
logger.config(verbose=0)
```

```python
import mootdx
mootdx.logger.config(verbose=0)
```
