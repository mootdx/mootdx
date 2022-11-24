import asyncio
import functools
import json
import socket
import time
from functools import partial

from tdxpy.constants import hq_hosts
from tdxpy.exhq import TdxExHq_API
from tdxpy.hq import TdxHq_API

from mootdx.consts import CONFIG
from mootdx.consts import EX_HOSTS
from mootdx.consts import GP_HOSTS
from mootdx.logger import logger
from mootdx.utils import get_config_path

hosts = {
    "HQ": [{"addr": hs[1], "port": hs[2], "time": 0, "site": hs[0]} for hs in hq_hosts + GP_HOSTS],
    "EX": [{"addr": hs[1], "port": hs[2], "time": 0, "site": hs[0]} for hs in EX_HOSTS],
    "GP": [{"addr": hs[1], "port": hs[2], "time": 0, "site": hs[0]} for hs in GP_HOSTS],
}

results = {k: [] for k in hosts}


def callback(res, key):
    """
    异步回调函数

    :param res:
    :param key:
    """
    result = res.result()

    if result.get("time"):
        results[key].append(result)

    # logger.debug(f"callback: {res.result()}")


def connect(proxy: dict) -> dict:
    """
    连接服务器函数

    :param proxy: 代理IP信息
    :return:
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(.7)

        start = time.perf_counter()

        sock.connect((proxy.get("addr"), int(proxy.get("port"))))
        sock.close()

        proxy["time"] = (time.perf_counter() - start) * 1000

        logger.debug("{addr}:{port} 验证通过，响应时间：{time} ms.".format(**proxy))
    except socket.timeout as ex:
        logger.debug("{addr},{port} time out.".format(**proxy))
        proxy["time"] = None
    except ConnectionRefusedError as ex:
        logger.debug("{addr},{port} 验证失败.".format(**proxy))
        proxy["time"] = None

    return proxy


def connect2(proxy, index='HQ'):
    if index == 'GP':
        return connect(proxy)

    api = (TdxHq_API(), TdxExHq_API())[index != 'HQ']
    fun = ('get_security_count', 'get_instrument_count')[index != 'HQ']

    proxy["time"] = None

    try:
        with api.connect(proxy.get("addr"), int(proxy.get("port")), time_out=0.7):
            tms = time.perf_counter()
            if getattr(api, fun)():
                proxy["time"] = (time.perf_counter() - tms) * 1000
                logger.debug("{addr}:{port} 验证通过，响应时间：{time} ms.".format(**proxy))
            else:
                logger.debug("{addr}:{port} 验证失败.".format(**proxy))
    except socket.timeout as ex:
        logger.debug("{addr}:{port} time out.".format(**proxy))
        proxy["time"] = None
    except Exception as e:
        logger.debug("{addr}:{port} 验证失败.".format(**proxy))

    return proxy


async def verify(proxy: dict, index):
    """
    检验代理连通性函数

    :param proxy: 代理IP信息
    :return:
    """
    return await asyncio.get_event_loop().run_in_executor(None, functools.partial(connect2, proxy=proxy, index=index))


def server(index=None, limit=5, console=False, sync=True):
    _hosts = hosts[index]

    def async_event():
        event = asyncio.get_event_loop()
        tasks = []

        while len(_hosts) > 0:
            task = event.create_task(verify(_hosts.pop(0), index))
            task.add_done_callback(partial(callback, key=index))
            tasks.append(task)

        # event.is_closed()
        # event.is_running()
        event.run_until_complete(asyncio.wait(tasks))

    global results

    if sync:
        results[index] = [connect(proxy) for proxy in _hosts]
        results[index] = [x for x in results[index] if x.get("time")]
    else:
        async_event()

    server = results[index]

    # 结果按响应时间从小到大排序
    if console:
        from prettytable import PrettyTable

        server.sort(key=lambda item: item["time"])

        if limit:
            server = server[:limit]

        logger.debug("[√] 最优服务器:")

        t = PrettyTable(["Name", "Addr", "Port", "Time"])
        t.align["Name"] = "l"
        t.align["Addr"] = "l"
        t.align["Port"] = "l"
        t.align["Time"] = "r"
        t.padding_width = 1

        for host in server:
            t.add_row(
                [
                    host["site"],
                    host["addr"],
                    host["port"],
                    "{:5.2f} ms".format(host["time"]),
                ]
            )

        logger.debug("\n" + str(t))

    return [(item["addr"], item["port"]) for item in server]


def check_server(console=False, limit=5, sync=False) -> None:
    return bestip(console=console, limit=limit, sync=sync)


def bestip(console=False, limit=5, sync=False) -> None:
    config_ = get_config_path("config.json")
    default = dict(CONFIG)

    logger.info("[-] 选择最快的服务器...")
    logger.debug(f'sync => {sync}')

    for index in ["HQ", "EX", "GP"]:
        try:
            data = server(index=index, limit=limit, console=console, sync=sync)

            if data:
                default["BESTIP"][index] = data[0]
        except RuntimeError as ex:
            logger.error("请手动运行`python -m mootdx bestip`")
            break

    json.dump(default, open(config_, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


if __name__ == "__main__":
    bestip(sync=False, limit=5, console=True)
