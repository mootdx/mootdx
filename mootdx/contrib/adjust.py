import json
import re
import time
import pandas as pd
import httpx
from numpy import asarray

from mootdx.logger import log


def get_adjust_year(symbol=None, year='2021', factor='00'):
    """
    采集同花顺复权数据

    # http://d.10jqka.com.cn/v2/line/hs_600036/01/2018.js
    # http://d.10jqka.com.cn/v6/line/hs_600000/00/all.js

    :param symbol: 股票代码
    :param factor: 前后复权 before 或 01 为前复权， after 或 02为后复权
    :param year: 年份
    :return: DataFrame
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Referer': 'http://stockpage.10jqka.com.cn/',
        'DNT': '1',
    }

    client = httpx.Client(transport=httpx.HTTPTransport(retries=5))

    if factor == 'before':
        factor = '01'

    if factor == 'after':
        factor = '02'

    if factor not in ['01', '02']:
        log.warning('复权参数错误，factor 的值必须是: before, after, 01, 02')
        return pd.DataFrame(data=None)

    i = 0

    while i < 3:
        try:
            url = f'http://d.10jqka.com.cn/v2/line/hs_{symbol}/{factor}/{year}.js'
            res = client.get(url, headers=headers)
            res.raise_for_status()

            # 出现 window.location.href 则请求太频繁，需要稍等再采集
            text = re.findall(r'\((.*)\)', res.text)[0]
            text = json.loads(text)

            data = text['data'].split(';')
            data = [item.split(',')[:8] for item in data]

            columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'amount', 'adjust']
            return pd.DataFrame(data, index=list(asarray(data).T[0]), columns=columns)
        except httpx.HTTPError:
            log.warning('网络连接失败，请重试...')
        except httpx.RequestError:
            log.warning('网络连接失败，请重试...')
        except IndexError as e:
            log.warning('数据解析错误，请求太频繁，请稍后重试...')
            log.debug(e)
        finally:
            time.sleep(.2)
            i += 1

    return pd.DataFrame(data=None)
