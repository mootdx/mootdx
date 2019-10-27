# -*- coding: utf-8 -*-
import logging
import socket
import threading
import time

from prettytable import PrettyTable

from mootdx.consts import hq_hosts, ex_hosts, gp_hosts

logger = logging.getLogger(__name__)
result = []
hosts = {
    'hq': [{'addr': hs[1], 'port': hs[2], 'time': 0, 'site': hs[0]} for hs in hq_hosts],
    'ex': [{'addr': hs[1], 'port': hs[2], 'time': 0, 'site': hs[0]} for hs in ex_hosts],
    'gp': [{'addr': hs[1], 'port': hs[2], 'time': 0, 'site': hs[0]} for hs in gp_hosts],
}

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
def get_hosts(index):
    global hosts

    if len(hosts[index]) > 0:
        return hosts[index].pop()
    else:
        return ''


# 保存验证结果
@synchronous
def saveresult(proxy):
    global result

    if not (proxy in result):
        result.append(proxy)


# 线程函数
def verify(index='hq'):
    while True:
        proxy = get_hosts(index=index)

        # 所有行情均已验证完毕
        if len(proxy) == 0:
            return

        # 验证行情的可用性
        # 创建一个TCP连接套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 设置5超时
        sock.settimeout(5)

        try:
            start = time.clock()

            # 连接行情服务器
            sock.connect((proxy.get('addr'), int(proxy.get('port'))))
            sock.close()

            proxy['time'] = (time.clock() - start) * 1000

            saveresult(proxy)

            logger.info("{}:{} 验证通过，响应时间：{:.2} ms.".format(proxy.get('addr'), proxy.get('port'), proxy.get('time')))
        except Exception:
            logger.warning("{},{} 验证失败.".format(proxy.get('addr'), proxy.get('port')))


def Server(limit=10, market='hq', verbose=False):
    if verbose:
        logging.basicConfig(level='DEBUG')

    print("[!] 开始测试线路...")

    thread_pool = []

    for i in range(20):
        th = threading.Thread(target=verify(market), args=())
        thread_pool.append(th)

    # start threads one by one
    for thread in thread_pool:
        thread.start()

    # collect all threads
    for thread in thread_pool:
        threading.Thread.join(thread)

    # 结果按响应时间从小到大排序
    result.sort(key=lambda item: (item['time']))

    print("[√] 最优服务器:")

    t = PrettyTable(["Name", "Addr", "Port", "Time"])
    t.align["Name"] = "l"
    t.align["Addr"] = "l"
    t.align["Port"] = "l"
    t.align["Time"] = "r"
    t.padding_width = 1

    for host in result[:int(limit)]:
        t.add_row([host['site'], host['addr'], host['port'], '%.2fms' % host['time']])

    print(t)

    return [(item['addr'], item['port']) for item in result]
