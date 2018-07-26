# -*- coding: utf-8 -*-
import logging
import socket
import threading
import time

import coloredlogs
from prettytable import PrettyTable
from pytdx.config.hosts import hq_hosts

logger = logging.getLogger(__name__)
# coloredlogs.install(fmt='[%(asctime)s] %(levelname)s %(message)s')

result = []
hosts = []

for x in hq_hosts:
    hosts.append({'addr': x[1], 'port': x[2], 'time': 0, 'site': x[0]})

# 线程同步锁
lock = threading.Lock()


def synchronous(f):
    def call(*args, **kwargs):
        lock.acquire()

        try:
            return f(*args, **kwargs)
        finally:
            lock.release()

    return call


# 获取一个待验证行情
@synchronous
def get_hosts():
    global hosts

    if len(hosts) > 0:
        return hosts.pop()
    else:
        return ''


# 保存验证结果
@synchronous
def saveresult(proxy):
    global result

    if not (proxy in result):
        result.append(proxy)


# 线程函数
def verify():
    while True:
        proxy = get_hosts()
        # 所有行情均已验证完毕
        if len(proxy) == 0:
            return

        # 验证行情的可用性
        # 创建一个TCP连接套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 设置10超时
        sock.settimeout(5)

        try:
            start = time.clock()

            # 连接行情服务器
            sock.connect((proxy['addr'], int(proxy['port'])))
            sock.close()

            proxy['time'] = (time.clock() - start) * 1000

            saveresult(proxy)

            logger.debug("%s:%s 验证通过，响应时间：%d ms." %
                         (proxy['addr'], proxy['port'], proxy['time']))
        except Exception as e:
            logger.error("%s,%s 验证失败." % (proxy['addr'], proxy['port']))


def check(limit=10, verbose=False, tofile=''):
    # init thread_pool
    if verbose:
        # coloredlogs.install(level='DEBUG', logger=logger)
        coloredlogs.install(level='DEBUG', logger=logger, fmt='[%(asctime)s] %(levelname)s %(message)s')

    thread_pool = []

    for i in range(20):
        th = threading.Thread(target=verify, args=())
        thread_pool.append(th)

    # start threads one by one
    for thread in thread_pool:
        thread.start()

    # collect all threads
    for thread in thread_pool:
        threading.Thread.join(thread)

    # 结果按响应时间从小到大排序
    # result.sort(lambda x, y: cmp(x['time'], y['time']))
    result.sort(key=lambda x: (x['time']))

    print("最优服务器:")

    t = PrettyTable(["Name", "Addr", "Port", "Time"])
    t.align["Name"] = "l"
    t.align["Addr"] = "l"
    t.align["Port"] = "l"
    t.align["Time"] = "r"
    t.padding_width = 1

    for x in result[:int(limit)]:
        t.add_row([x['site'], x['addr'], x['port'], '%.2fms' % x['time']])

    print(t)


if __name__ == '__main__':
    check()
