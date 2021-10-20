import asyncio
import functools
import json
import socket
import time
from functools import partial

from mootdx.consts import CONFIG
from mootdx.consts import EX_HOSTS
from mootdx.consts import GP_HOSTS
from mootdx.consts import HQ_HOSTS
from mootdx.logger import log
from mootdx.utils import get_config_path

hosts = {
    'HQ': [{'addr': hs[1], 'port': hs[2], 'time': 0, 'site': hs[0]} for hs in HQ_HOSTS],
    'EX': [{'addr': hs[1], 'port': hs[2], 'time': 0, 'site': hs[0]} for hs in EX_HOSTS],
    'GP': [{'addr': hs[1], 'port': hs[2], 'time': 0, 'site': hs[0]} for hs in GP_HOSTS],
}

results = {k: [] for k in hosts}


def callback(res, key):
    result = res.result()

    if result.get('time'):
        results[key].append(result)

    log.debug('callback: {}', res.result())


def connect(proxy):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)

        start = time.perf_counter()

        sock.connect((proxy.get('addr'), int(proxy.get('port'))))
        sock.close()

        proxy['time'] = (time.perf_counter() - start) * 1000

        log.info('{addr}:{port} 验证通过，响应时间：{time} ms.'.format(**proxy))
    except socket.timeout as ex:
        log.info('{addr},{port} time out.'.format(**proxy))
        proxy['time'] = None
    except ConnectionRefusedError as ex:
        log.info('{addr},{port} 验证失败.'.format(**proxy))
        proxy['time'] = None
    finally:
        return proxy


async def verify(proxy):
    result = await asyncio.get_event_loop().run_in_executor(None, functools.partial(connect, proxy=proxy))
    return result


def Server(index=None, limit=5, console=False, sync=True):
    _hosts = hosts[index]

    def async_event():
        event = asyncio.get_event_loop()
        tasks = []

        while len(_hosts) > 0:
            task = event.create_task(verify(_hosts.pop(0)))
            task.add_done_callback(partial(callback, key=index))
            tasks.append(task)

        # event.is_closed()
        # event.is_running()
        event.run_until_complete(asyncio.wait(tasks))

    global results

    if sync:
        results[index] = [connect(proxy) for proxy in _hosts]
        results[index] = [x for x in results[index] if x.get('time')]
    else:
        async_event()

    server = results[index]

    # 结果按响应时间从小到大排序
    if console:
        from prettytable import PrettyTable

        server.sort(key=lambda item: item['time'])
        print('[√] 最优服务器:')

        t = PrettyTable(['Name', 'Addr', 'Port', 'Time'])
        t.align['Name'] = 'l'
        t.align['Addr'] = 'l'
        t.align['Port'] = 'l'
        t.align['Time'] = 'r'
        t.padding_width = 1

        for host in server[: int(limit)]:
            t.add_row(
                [
                    host['site'],
                    host['addr'],
                    host['port'],
                    '{:5.2f} ms'.format(host['time']),
                ]
            )

        print(t)

    return [(item['addr'], item['port']) for item in server]


def bestip(console=False, limit=5, sync=True) -> None:
    config_ = get_config_path('config.json')
    default = dict(CONFIG)

    for index in ['HQ', 'EX', 'GP']:
        try:
            data = Server(index=index, limit=limit, console=console, sync=sync)
            if data:
                default['BESTIP'][index] = data[0]
        except RuntimeError as ex:
            log.error('请手动运行`python -m mootdx bestip`')
            break

    json.dump(default, open(config_, 'w'), indent=2, ensure_ascii=False)


if __name__ == '__main__':
    bestip()
