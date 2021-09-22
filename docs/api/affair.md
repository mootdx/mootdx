## 01. 财务数据列表

> 财务数据相关字段，请参见 [财务数据字段对照表](fields.md)

实现了历史财务数据列表的读取，使用方式

```python
from mootdx.affair import Affair

Affair.files()
```

结果:

```
Out[17]:
 [{'filename': 'gpcw19990630.zip',
  'hash': '65228d9db21d42e683698ac8dd72ef57',
  'filesize': 443065},
 {'filename': 'gpcw19981231.zip',
  'hash': 'adbed98b12cbc1c4ac312ff9d0fd4b69',
  'filesize': 639007},
 {'filename': 'gpcw19980630.zip',
  'hash': 'eddfbcc712aae4f3f79acee4afba6787',
  'filesize': 385920}

  .....]
```

其中，`filename` 字段为具体的财务数据文件地址， 后面的分别是哈希值和文件大小，在同步到本地时，可以作为是否需要更新本地数据的参考

## 02. 历史数据内容

获取历史专业财务数据内容

使用上面返回的`filename`字段作为参数即可

```python
from mootdx.affair import Affair

Affair.fetch(downdir='output', filename='gpcw20170930.zip')
```

## 03. 解析本地数据

如果您自己管理文件的下载或者本地已经有对应的数据文件，同时支持`.zip`和解压后的`.dat`文件. 如果扩展名不写，则自动判断存在的文件.

```python
from mootdx.affair import Affair

data = Affair.parse(downdir='output', filename='gpcw20170930.zip')
```

## 04. 保存到文件

代码方式

```python
from mootdx.affair import Affair

result = Affair.parse(downdir='output', filename='gpcw20170930.zip')

# 保存 csv 文件
result.to_csv('gpcw20170930.csv')

# 保存 Excel 文件
result.to_excel('gpcw20170930.xls')
```

命令行方式

写入到文件 : `gpcw20170930.csv`

```shell
mootdx affair -f gpcw20000930.zip -o gpcw20170930.csv
```
