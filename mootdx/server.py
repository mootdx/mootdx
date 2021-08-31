# -*- coding: utf-8 -*-
import json
import socket
import sys
import time

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


def Server(index=None, limit=5, console=False, verbose=False):
    if verbose:
        log.add(sys.stdout, level="DEBUG")

    _hosts = hosts[index]

    server = []

    while len(_hosts) > 0:

        proxy = _hosts.pop()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)

        try:
            start = time.perf_counter()

            sock.connect((proxy.get("addr"), int(proxy.get("port"))))
            sock.close()

            proxy["time"] = (time.perf_counter() - start) * 1000

            server.append(proxy)

            log.debug(
                "{}:{} 验证通过，响应时间：{:5.2f} ms.".format(
                    proxy.get("addr"), proxy.get("port"), proxy.get("time")
                )
            )
        except Exception as e:
            log.debug("{},{} 验证失败.".format(proxy.get("addr"), proxy.get("port")))

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


def bestip(verbose=False, console=False, limit=5) -> None:
    config_ = get_config_path("config.json")
    default = dict(CONFIG)

    for index in ["HQ", "EX", "GP"]:
        data = Server(index=index, limit=limit, console=console, verbose=verbose)
        if data:
            default["BESTIP"][index] = data[0]

    json.dump(default, open(config_, "w"), indent=2)
    config.setup()
