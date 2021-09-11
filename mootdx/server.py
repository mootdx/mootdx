# -*- coding: utf-8 -*-
import asyncio
import functools
import json
import socket
import time
from functools import partial

from mootdx import config
from mootdx.consts import CONFIG
from mootdx.consts import EX_HOSTS
from mootdx.consts import GP_HOSTS
from mootdx.consts import HQ_HOSTS
from mootdx.logger import log
from mootdx.utils import get_config_path

hosts = {
    "HQ": [{"addr": hs[1], "port": hs[2], "time": 0, "site": hs[0]} for hs in HQ_HOSTS],
    "EX": [{"addr": hs[1], "port": hs[2], "time": 0, "site": hs[0]} for hs in EX_HOSTS],
    "GP": [{"addr": hs[1], "port": hs[2], "time": 0, "site": hs[0]} for hs in GP_HOSTS],
}


def callback(res):
    print(res)


async def verify(proxy):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)

        start = time.perf_counter()

        sock.connect((proxy.get("addr"), int(proxy.get("port"))))
        sock.close()

        proxy["time"] = (time.perf_counter() - start) * 1000

        log.debug(
            "{}:{} 验证通过，响应时间：{:5.2f} ms.".format(
                proxy.get("addr"), proxy.get("port"), proxy.get("time")
            )
        )
    except socket.timeout as ex:
        log.exception(ex)
    except ConnectionRefusedError as ex:
        log.exception(ex)
        log.debug("{addr},{port} 验证失败.".format(**proxy))
    finally:
        return proxy


def Server(index=None, limit=5, console=False):
    _hosts = hosts[index]

    log.warning(_hosts)

    server = []

    tasks = []

    loop = asyncio.get_event_loop()

    while len(_hosts) > 0:
        task = loop.create_task((verify(_hosts.pop(0))))
        task.add_done_callback(partial(callback))
        tasks.append(task)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    # 结果按响应时间从小到大排序
    if console:
        from prettytable import PrettyTable

        server.sort(key=lambda item: item["time"])
        print("[√] 最优服务器:")

        t = PrettyTable(["Name", "Addr", "Port", "Time"])
        t.align["Name"] = "l"
        t.align["Addr"] = "l"
        t.align["Port"] = "l"
        t.align["Time"] = "r"
        t.padding_width = 1

        for host in server[: int(limit)]:
            t.add_row(
                [
                    host["site"],
                    host["addr"],
                    host["port"],
                    "{:5.2f} ms".format(host["time"]),
                ]
            )

        print(t)

    return [(item["addr"], item["port"]) for item in server]


async def _get_requests(proxy):
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, functools.partial(verify, proxy=proxy))
    return r, proxy


async def _get_docker_index_info(context, proxies):
    tasks = [asyncio.ensure_future(_get_requests(proxy)) for proxy in proxies]

    for task in asyncio.as_completed(tasks):
        r, key = await task

        if r.status_code == 200:
            context[key] = r.json()

    return context


def get_context_data(**kwargs):
    context = get_context_data(**kwargs)
    loop = asyncio.new_event_loop()
    task = loop.create_task(_get_docker_index_info(context, EX_HOSTS))
    loop.run_until_complete(task)
    context = task.result()
    return context


def bestip(console=False, limit=5) -> None:
    config_ = get_config_path("config.json")
    default = dict(CONFIG)

    for index in ["HQ", "EX", "GP"]:
        data = Server(index=index, limit=limit, console=console)
        if data:
            default["BESTIP"][index] = data[0]

    json.dump(default, open(config_, "w"), indent=2)
    config.setup()
