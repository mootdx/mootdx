# 辅助工具函数

## 01. 获取同花顺复权数据

可以按年份获取单只股票的复权行情数据 (自己计算复权蛋疼的不行，这个诸位先用着吧 😀)

**参数说明: **

- symbol: 股票代码。 `"600300"` 格式
- factor: 前后复权。 `"00"`: 不复权, `"01"`: 前复权, `"02"`: 后复权
- year: 获取数据的年份。 `"2021"` 格式, 默认当前年份

返回值：

- pd.DataFrame

**调用方法：**

```python
from mootdx.contrib.adjust import get_adjust_year

get_adjust_year(symbol='000001', year='2021', factor='01')
```

以下为返回内容格式

```shell
Out[2]:
             open   high    low  close     volume         amount adjust
date
2021-01-04  18.92  18.92  18.26  18.42  155421640  2891682300.00  0.801
2021-01-05  18.22  18.30  17.62  17.99  182135210  3284606900.00  0.939
2021-01-06  17.90  19.38  17.82  19.38  193494510  3648521900.00  0.997
2021-01-07  19.34  19.80  19.05  19.72  158418530  3111274600.00  0.816
2021-01-08  19.72  19.92  19.13  19.67  119547322  2348316400.00  0.616
...           ...    ...    ...    ...        ...            ...    ...
2021-09-02  18.00  18.78  17.80  18.40  242260350  4454545300.00  1.248
2021-09-03  18.50  18.50  17.70  18.04  139481870  2523273200.00  0.719
2021-09-06  17.93  18.60  17.78  18.45  151522560  2780281100.00  0.781
2021-09-07  18.60  19.56  18.35  19.24  162234420  3067365700.00  0.836
2021-09-08  19.24  19.55  19.10  19.31   88944393  1716830500.00  0.458

[168 rows x 7 columns]
```

## 02. TDX导出数据转为 pandas 可用的 csv 文件

将TDX通过数据工具导出的txt文件转换为标准的csv文件(其实不转回pandas 也可以读取，只是使用时候比较麻烦)

**参数说明: **

- infile: 输入文件
- outfile: 转换后的文件，可为空

返回值：

- pd.DataFrame

**调用方法：**

```python
from mootdx.tools import tdx2csv

tdx2csv.txt2csv(infile='sz#000001.txt', outfile='sz#000001.csv')
```

## 03. TDX导出数据转为 pandas 可用的 csv 文件(批量异步接口)

将TDX通过数据工具导出的txt文件转换为标准的csv文件(其实不转回pandas 也可以读取，只是使用时候比较麻烦)

**参数说明: **

- src: 要换行的目录(tdx导出文件目录)
- dst: 转换后的目录

返回值：

- None

**调用方法：**

```python
from mootdx.tools import tdx2csv

tdx2csv.batch(src='c:/tdx/export', dst='c:/tdx/output')
```

## 04. 交易日是否法定节假日

参数说明:

- date: 日期, 字符格式
- format_: 日期格式 默认: %Y-%m-%d (e: 2010-01-01)
- country: 国家, 默认: 中国

返回值：

- 布尔值, True 为法定节假日, False 不是法定节假日

**调用方法：**

```python
from mootdx.utils import holiday

# 判断一个日期是否是法定节假日
holiday.holiday(date='20200202', format_='%Y%m%d', country='中国')

# 判断一个日期是否是法定节假日
holiday.holiday(date='2020-02-02')

# 判断当天日期是否是法定节假日（date的值空为当天日期）
holiday.holiday()
```

## 05. 新版自定义板块操作

参数说明:

- name: 板块名称
- symbol: 股票代码列表
- tdxdir: 通达信的安装目录

返回值：

- 布尔值, True 成功, False 失败

**调用方法：**

```python
from mootdx.contrib.customize import Customize

# 初始化一个自定义版本操作对象, tdxdir 可根据具体情况修改
custom = Customize(tdxdir='C:/new_tdx')

# 新建自定义板块
custom.create(name='龙虎榜', symbol=['600036', '600016'])

# 再创建一个, 板块名称不能重复
custom.create(name='优质股', symbol=['600036', '600016'])

# 修改自定义板块
custom.update(name='龙虎榜', symbol=['600036', '600016'])

# 查询自定义板块
custom.search(name='龙虎榜')

# 删除指定名称的自定义板块
custom.remove(name='龙虎榜')

```
