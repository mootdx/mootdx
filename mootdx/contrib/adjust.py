import json
import re

import numpy as np
import pandas as pd
import requests


# 00 不复权 01前复权 02后复权
# recover = before after
def get_k_adjust_year(symbol=None, year=None, recover='00'):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'Upgrade-Insecure-Requests':
            '1'
    }

    url = f'http://d.10jqka.com.cn/v2/line/hs_{symbol}/{recover}/{year}.js'
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        print(resp.content)
        return None

    text = re.findall(r'\((.*)\)', resp.text)[0]
    text = json.loads(text)
    data = text['data'].split(';')
    data = [item.split(',')[:8] for item in data]

    columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'amount', 'factor']
    return pd.DataFrame(data, index=list(np.asarray(data).T[0]), columns=columns)


if __name__ == '__main__':
    for x in range(2000, 2019):
        for fq in ('00', '01', '02'):
            print(get_k_adjust_year('000001', str(x), fq))
            print(get_k_adjust_year('600010', str(x), fq))
