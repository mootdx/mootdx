
# 历史专业财务数据

## 参考信息

- issue from @datochan [https://github.com/rainx/mootdx/issues/133](https://github.com/rainx/mootdx/issues/133)
- [通达信专业财务函数文档](http://www.tdx.com.cn/products/helpfile/tdxw/chm/%E7%AC%AC%E4%B8%89%E7%AB%A0%20%20%20%E5%9F%BA%E7%A1%80%E5%8A%9F%E8%83%BD/3-3/3-3-2/3-3-2-15/3-3-2-15.html)

## mootdx.crawler

`crawler` 其实本来想叫做`downloader`或者`fetcher`, 专门来处理http 协议(现在也支持tcp的方式获取）的数据的下载和解析，分为两个阶段，下载阶段我们会使用urllib来下载数据，数据可以下载到临时文件（不传入`path_to_download`参数）或者下载到指定的位置（提供`path_to_download`参数），也支持指定chunk的分段下载进度的提示（使用`reporthook`传入处理函数）， 下面是一个reporthook函数的例子

```python
def reporthook(downloaded=None, total_size):
    print("#", end='')

```

## 获取历史数据

mootdx.crawler.HistoryFinancialListCrawler

实现了历史财务数据列表的读取，使用方式

```python
from mootdx.affairs import Affairs
Affairs.fetch(downdir='output')

结果:

+------------------+----------+----------------------------------+
| filename         | filesize | hash                             |
+------------------+----------+----------------------------------+
| gpcw20191231.zip | 165      | b590fc5fa3a6ec6ab5d881c31e1d71a5 |
| gpcw20190930.zip | 735606   | e9059088e8031b3407e84bb536be365a |
| gpcw20190630.zip | 3213061  | 13d2729685d65efebb0d6b47c4c16b40 |
| gpcw20190331.zip | 2859099  | 95724f55c9a20be3c7bd1cea95919ed8 |
| gpcw20181231.zip | 3274511  | 585ffa351f4060e6274bdfb9d36de097 |
| gpcw20180930.zip | 2927452  | 4f463b8536cea8fcaaec90512a562dae |
| gpcw20180630.zip | 3085199  | a6381831231a782cf193285b6fb4b22d |
| gpcw20180331.zip | 2722534  | 0835660cce80028fd59131e7c5f5f75e |
| gpcw20171231.zip | 3188864  | 572f1c558cf48e149d7e065aba5fe787 |
| gpcw20170930.zip | 2810523  | 1118a83cdcb0c5cfc966aa83b9d0f8dd |
| gpcw20170630.zip | 2938359  | dff36b6f878a38e7ddc5fffb6e23d98b |
| gpcw20170331.zip | 2512854  | eb877c7dcedc72eba27cd21610e19bd5 |
| gpcw20161231.zip | 3092803  | 2d50e15bec7ee813f23160c01e626d98 |
| gpcw20160930.zip | 2486170  | 97eca7c59b9254e09df0c3efa8b9ff53 |

```

其中，`filename` 字段为具体的财务数据文件地址， 后面的分别是哈希值和文件大小，在同步到本地时，可以作为是否需要更新本地数据的参考

## 获取历史数据内容

mootdx.crawler.HistoryFinancialCrawler

获取历史专业财务数据内容

使用上面返回的`filename`字段作为参数即可

```python
from mootdx.affairs import Affairs
Affairs.fetch(downdir='output', filename='gpcw20170930.zip')

```

## 解析本地数据

如果您自己管理文件的下载或者本地已经有对应的数据文件，可以使用我们的 `HistoryFinancialReader`来读取本地数据，使用方法和其它的Reader是类似的, 我们的reader同时支持`.zip`和解压后的`.dat`文件

```python
from mootdx.affairs import Affairs

data = Affairs.parse(downdir='output', filename='gpcw20170930.zip')

```

## 通过命令行工具`hq_reader`读取并保存到csv文件

```
$ mootdx affair -f gpcw20000930.zip -o gpcw20170930.csv

写入到文件 : gpcw20170930.csv
```
