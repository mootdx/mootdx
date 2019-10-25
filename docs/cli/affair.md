
# 历史专业财务数据

## 参考

- issue from @datochan [https://github.com/rainx/mootdx/issues/133](https://github.com/rainx/mootdx/issues/133)
- [通达信专业财务函数文档](http://www.tdx.com.cn/products/helpfile/tdxw/chm/%E7%AC%AC%E4%B8%89%E7%AB%A0%20%20%20%E5%9F%BA%E7%A1%80%E5%8A%9F%E8%83%BD/3-3/3-3-2/3-3-2-15/3-3-2-15.html)

## mootdx.crawler

`crawler` 其实本来想叫做`downloader`或者`fetcher`, 专门来处理http 协议(现在也支持tcp的方式获取）的数据的下载和解析，分为两个阶段，下载阶段我们会使用urllib来下载数据，数据可以下载到临时文件（不传入`path_to_download`参数）或者下载到指定的位置（提供`path_to_download`参数），也支持指定chunk的分段下载进度的提示（使用`reporthook`传入处理函数）， 下面是一个reporthook函数的例子

```bash
$ mootdx affair --help

Usage: mootdx affair [OPTIONS]

  财务文件下载&解析.

Options:
  -p, --parse TEXT    解析文件内容
  -l, --files         列出文件列表
  -f, --fetch TEXT    下载全部文件
  -o, --output TEXT   输出文件
  -d, --downdir TEXT  下载文件目录
  -v, --verbose
  --help              Show this message and exit.
```

```bash
$ mootdx affair -l


+------------------+----------+----------------------------------+
| filename         | filesize | hash                             |
+------------------+----------+----------------------------------+
| gpcw20191231.zip | 165      | b590fc5fa3a6ec6ab5d881c31e1d71a5 |
| gpcw20190930.zip | 735575   | 16e8f046362e951d154b1f5290137845 |
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
| gpcw20160630.zip | 2551679  | f9289299b7d2f485d6adbe8fafccd63c |
| gpcw20160331.zip | 2159096  | 86940ff11443db8348890c96131442f8 |
| gpcw20151231.zip | 2903744  | 1c8f3a10be622e04dfeeb62fae2dd68a |
| gpcw20150930.zip | 2187757  | 82616398af3f7808752373039ba85916 |
| gpcw20150630.zip | 2287108  | 13b883f6cb1535cfce6817571cf4f5ec |
| gpcw20150331.zip | 2003985  | 354ab4cb5eed01a70cd4ecb23ecafb5e |
| gpcw20141231.zip | 2745200  | 3d6c6455a1d8a623273f626a07b991b6 |
| gpcw20140930.zip | 2002886  | 52dfe78a609a1e0cb4cb5afcfa737e9b |
| gpcw20140630.zip | 2080114  | 1fe84c5191cd332d09caca78be725a91 |
| gpcw20140331.zip | 1808309  | f09a43d36dfffb834a13d232d5886ba8 |
| gpcw20131231.zip | 2439182  | ff37248582c41aae07411f99627f75c0 |
| gpcw20130930.zip | 1876566  | e0e9ef2bbf5f109ee8b3bd0b0f142b5d |
| gpcw20130630.zip | 1991372  | 972e85e229c0734f1f83d3a495593031 |
| gpcw20130331.zip | 1740962  | 6717844ad7d29955643ad86c24605f06 |
| gpcw20121231.zip | 2212652  | af9e231c85fed71ba230f64da55f6156 |
| gpcw20120930.zip | 1835884  | 84a1a0337f0e75ac0dcf9d954296b60c |
| gpcw20120630.zip | 1925970  | ef4c783754ba14f243cc6331738f2e8b |
| gpcw20120331.zip | 1675642  | d3eda9a30447539648207306b9b0cd81 |
| gpcw20111231.zip | 2051000  | a3aed02fac4737d9618c44e479f94ad2 |
| gpcw20110930.zip | 1705852  | f3d45df6fa55a4558b48b66ad626f013 |
| gpcw20110630.zip | 1796397  | 64df1e149bda9ba1e27754dca56ddcc1 |
| gpcw20110331.zip | 1498382  | 7954fef73d29b7e193ca0d952ab4eec6 |
| gpcw20101231.zip | 1941963  | c65439ac77dcd22683ef92f966054412 |
| gpcw20100930.zip | 1497433  | 7ac51ec65570a0ffee0dd5ff76b68974 |
| gpcw20100630.zip | 1570846  | 2945b478d995a71c26ac59d34f98fe42 |
| gpcw20100331.zip | 1262002  | 3d134801971d48228b08a26a5e8a232b |
| gpcw20091231.zip | 1851135  | b7aa3d8446d9ad15386be402577ff643 |
| gpcw20090930.zip | 1218815  | c174d3f6624e1810130084827557032c |
| gpcw20090630.zip | 1306660  | 4d755d567f6adb332a7da6cc58ed1687 |
| gpcw20090331.zip | 1069769  | dd5578ee932abba7cd8562c111024e2b |
| gpcw20081231.zip | 1751973  | a1a9dc1a26d218bf862d28218eff44d8 |
| gpcw20080930.zip | 1123629  | 1a2078ee75b4f5d14afac356a989f598 |
| gpcw20080630.zip | 1216453  | 53162a52b777b0d6cbb1255c0f985b51 |
| gpcw20080331.zip | 1061851  | de3324b924e1a3b24c16df3b02f03225 |
| gpcw20071231.zip | 1552470  | 6b4d6e3be628df7f32a84cd7770522c9 |
| gpcw20070930.zip | 1065679  | a68a51e3d72b0351382d6b3f32621415 |
| gpcw20070630.zip | 1135930  | 2bb1f5bc84893f8128afb65aedbb32ac |
| gpcw20070331.zip | 961135   | 656639c0ba38b9d3fc0b0fef2fbfb6fd |
| gpcw20061231.zip | 1283336  | 73afdb49f1bf98cadec498041b8235d5 |
| gpcw20060930.zip | 1043520  | 77018ed1c9833c340925a55fde95b807 |
| gpcw20060630.zip | 1050173  | 51ddcb123c0e7ec92032d4550c7a2836 |
| gpcw20060331.zip | 938223   | 71a8ea03418a916766de5e5a683ea12b |
| gpcw20051231.zip | 1173316  | 146347dcb86a11f13851e37fa4cda605 |
| gpcw20050930.zip | 982826   | 8bb43fc34b3c70c68b0d8a012cdbb5b3 |
| gpcw20050630.zip | 996436   | d48b52c94e1bed62a80cddee8f2674ea |
| gpcw20050331.zip | 905884   | ce310a772f331dcbd28ebbb1821c0438 |
| gpcw20041231.zip | 1129778  | 560538f0aa4cd62c3c602d8eb3511b5b |
| gpcw20040930.zip | 960629   | 66216e46930b15720f8ee274674c188e |
| gpcw20040630.zip | 975181   | 95ce1e39be869b3da335e2806fb793d1 |
| gpcw20040331.zip | 852327   | 3084d863549519265569285b520bbcb1 |
| gpcw20031231.zip | 1036547  | ef910c6f171c80fd432a6efcec769b97 |
| gpcw20030930.zip | 826983   | 7c7d1ca5f9edf6a71395f6409ccb23e0 |
| gpcw20030630.zip | 842121   | 9a83a03c84b308ff250b7d019bea8b79 |
| gpcw20030331.zip | 743994   | 6fb6d9cd5578ce3f7a43a5760d953af8 |
| gpcw20021231.zip | 901615   | 33f2fa686f440d31fbdb5846edabdd4d |
| gpcw20020930.zip | 548230   | c8ef76f6c420c6519601cc29a74ce601 |
| gpcw20020630.zip | 787202   | 8e91ddc890de80b20d3532ef1562b462 |
| gpcw20020331.zip | 471926   | 12e03c59c06d8d2e3df780817c987687 |
| gpcw20011231.zip | 844044   | ec5e2b63a8a17c52089cac1f7eebd0a9 |
| gpcw20010930.zip | 47423    | fcd4222b9e82b442cd0e540e89e1e815 |
| gpcw20010630.zip | 710149   | 885a83565302443b532f2d93d8c98c49 |
| gpcw20010331.zip | 7407     | f1eb67155ed08009eb2dfb0c3f834a80 |
| gpcw20001231.zip | 793222   | a6e35c8922a7fe428318f60e9db6504d |
| gpcw20000930.zip | 654      | ef3183b7bc262321e5af768a9c990387 |
| gpcw20000630.zip | 654453   | 1af151900020f42b7fd2c814bfa8efa5 |
| gpcw19991231.zip | 730187   | ab144a39e36a6105aa0410e3e7cb899a |
| gpcw19990630.zip | 451364   | ca093c4b10b603efd0f86cf0f317e953 |
| gpcw19981231.zip | 639196   | f929cc7428320d37865d55ae1c114895 |
| gpcw19980630.zip | 386073   | b0589657867d967b61a390f5c5d9a458 |
+------------------+----------+----------------------------------+
```

```bash
$ mootdx affair -f gpcw20191231.zip

Downloaded 165, Total is 0
```


```bash
$ mootdx affair -f all

Downloaded 165, Total is 0
Downloaded 30000, Total is 0
Downloaded 60000, Total is 0
Downloaded 90000, Total is 0

....

```

```bash
$ mootdx affair -p gpcw20000930.zip

        report_date  col1  col2  ...        col313   col314        col315
code                             ...
600306     20000930   0.0   0.0  ... -4.039810e+34  31201.0 -4.039810e+34
600565     20000930   0.0   0.0  ... -4.039810e+34  81028.0 -4.039810e+34

[2 rows x 316 columns]
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
pd.set_option(&amp;apos;display.max_columns&amp;apos;, None)
### 这里默认已经切换成使用通达信proxy server，如果想切回http方式，需要设置 crawler.mode = "http"

### 如果使用默认的方式，下面的方法需要传入 filesize=实际文件大小，可以通过前面的接口获取到
result = datacrawler.fetch_and_parse(reporthook=demo_reporthook, filename=&amp;apos;gpcw19971231.zip&amp;apos;, path_to_download="/tmp/tmpfile.zip")
print(datacrawler.to_df(data=result))

```

## 通过reader 读取数据

如果您自己管理文件的下载或者本地已经有对应的数据文件，可以使用我们的 `HistoryFinancialReader`来读取本地数据，使用方法和其它的Reader是类似的, 我们的reader同时支持`.zip`和解压后的`.dat`文件

```
from mootdx.reader import HistoryFinancialReader

# print(HistoryFinancialReader().get_df(&amp;apos;/tmp/tmpfile.zip&amp;apos;))
print(HistoryFinancialReader().get_df(&amp;apos;/tmp/gpcw20170930.dat&amp;apos;))

```

## 通过命令行工具`hq_reader`读取并保存到csv文件

```
--&gt;rainx@JingdeMacBook-Pro:/tmp$ hqreader -d hf -o /tmp/gpcw20170930.csv /tmp/gpcw20170930.dat
写入到文件 : /tmp/gpcw20170930.csv

```
