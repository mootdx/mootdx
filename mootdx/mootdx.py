# -*- coding: utf-8 -*-
import datetime

from pytdx.hq import TdxHq_API


# K线种类
# 0 5分钟K线 
# 1 15分钟K线 
# 2 30分钟K线 
# 3 1小时K线 
# 4 日K线
# 5 周K线
# 6 月K线
# 7 1分钟
# 8 1分钟K线 
# 9 日K线
# 10 季K线
# 11 年K线

def ping(ip):
    api = TdxHq_API()
    __time1 = datetime.datetime.now()

    try:
        with api.connect(ip, 7709):
            if len(api.get_security_list(0, 1)) > 800:
                return datetime.datetime.now() - __time1
    except:
        print('Bad REPSONSE %s' % ip)
        return datetime.timedelta(9, 9, 0)


def best_ip():
    print('Selecting the Best Server IP of TDX')

    listx = ['218.75.126.9', '115.238.90.165',
             '124.160.88.183', '60.12.136.250', '218.108.98.244', '218.108.47.69',
             '14.17.75.71', '180.153.39.51']

    data = [ping(x) for x in listx]
    print('===The BEST SERVER is :  %s ===' % (listx[data.index(min(data))]))
    return listx[data.index(min(data))]
