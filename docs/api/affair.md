
# 历史专业财务数据

## 参考

- issue from @datochan [https://github.com/rainx/mootdx/issues/133](https://github.com/rainx/mootdx/issues/133)
- [通达信专业财务函数文档](http://www.tdx.com.cn/products/helpfile/tdxw/chm/%E7%AC%AC%E4%B8%89%E7%AB%A0%20%20%20%E5%9F%BA%E7%A1%80%E5%8A%9F%E8%83%BD/3-3/3-3-2/3-3-2-15/3-3-2-15.html)

## mootdx.crawler

`crawler` 其实本来想叫做`downloader`或者`fetcher`, 专门来处理http 协议(现在也支持tcp的方式获取）的数据的下载和解析，分为两个阶段，下载阶段我们会使用urllib来下载数据，数据可以下载到临时文件（不传入`path_to_download`参数）或者下载到指定的位置（提供`path_to_download`参数），也支持指定chunk的分段下载进度的提示（使用`reporthook`传入处理函数）， 下面是一个reporthook函数的例子

```

def demo_reporthook(downloaded, total_size):
    print("Downloaded {}, Total is {}".format(downloaded, total_size))

```

## 获取历史专业财务数据列表 mootdx.crawler.HistoryFinancialListCrawler

实现了历史财务数据列表的读取，使用方式

```
from mootdx.crawler.history_financial_crawler import HistoryFinancialListCrawler
crawler = HistoryFinancialListCrawler()

### 这里默认已经切换成使用通达信proxy server，如果想切回http方式，需要设置 crawler.mode = "http"
list_data = crawler.fetch_and_parse()
print(pd.DataFrame(data=list_data))

```

结果

```
In [8]: print(pd.DataFrame(data=list_data))
            filename  filesize                              hash
0   gpcw20171231.zip     49250  0370b2703a0e23b4f9d87587f4a844cf
1   gpcw20170930.zip   2535402  780bc7c649cdce35567a44dc3700f4ce
2   gpcw20170630.zip   2739127  5fef91471e01ebf9b5d3628a87d1e73d
3   gpcw20170331.zip   2325626  a9bcebff37dd1d647f3159596bc2f312
4   gpcw20161231.zip   2749415  3fb3018c235f6c9d7a1448bdbe72281a
5   gpcw20160930.zip   2262567  8b629231ee9fad7e7c86f1e683cfb489
..               ...       ...                               ...

75  gpcw19971231.zip    434680  316ce733f2a4f6b21c7865f94eee01c8
76  gpcw19970630.zip    196525  6eb5d8e5f43f7b19d756f0a2d91371f5
77  gpcw19961231.zip    363568  bfd59d42f9b6651861e84c483edb499b
78  gpcw19960630.zip    122145  18023e9f84565323874e8e1dbdfb2adb

[79 rows x 3 columns]

```

其中，`filename` 字段为具体的财务数据文件地址， 后面的分别是哈希值和文件大小，在同步到本地时，可以作为是否需要更新本地数据的参考

## 获取历史专业财务数据内容 mootdx.crawler.HistoryFinancialCrawler

获取历史专业财务数据内容

使用上面返回的`filename`字段作为参数即可

```
from mootdx.crawler.base_crawler import demo_reporthook
from mootdx.crawler.history_financial_crawler import HistoryFinancialCrawler

datacrawler = HistoryFinancialCrawler()
pd.set_option("display.max_columns", None)
### 这里默认已经切换成使用通达信proxy server，如果想切回http方式，需要设置 crawler.mode = "http"

### 如果使用默认的方式，下面的方法需要传入 filesize=实际文件大小，可以通过前面的接口获取到
result = datacrawler.fetch_and_parse(reporthook=demo_reporthook, filename="gpcw19971231.zip", path_to_download="/tmp/tmpfile.zip")
print(datacrawler.to_df(data=result))

```

## 通过 reader 读取数据

如果您自己管理文件的下载或者本地已经有对应的数据文件，可以使用我们的 `HistoryFinancialReader`来读取本地数据，使用方法和其它的Reader是类似的, 我们的reader同时支持`.zip`和解压后的`.dat`文件

```
from mootdx.reader import HistoryFinancialReader

# print(HistoryFinancialReader().get_df("/tmp/tmpfile.zip"))
print(HistoryFinancialReader().get_df("/tmp/gpcw20170930.dat"))

```

## 通过命令行工具`hq_reader`读取并保存到csv文件

```
--&gt;rainx@JingdeMacBook-Pro:/tmp$ hqreader -d hf -o /tmp/gpcw20170930.csv /tmp/gpcw20170930.dat
写入到文件 : /tmp/gpcw20170930.csv

```
