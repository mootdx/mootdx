"""TDX server discovery utilities.

Discovery is explicit and side-effect free until :func:`bestip` is called.
"""

from __future__ import annotations

import copy
import json
import socket
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from tdxpy.constants import hq_hosts
from tdxpy.exhq import TdxExHq_API
from tdxpy.exceptions import TdxConnectionError, TdxFunctionCallError
from tdxpy.hq import TdxHq_API

from mootdx.consts import CONFIG, EX_HOSTS, GP_HOSTS, HQ_HOSTS
from mootdx.logger import logger
from mootdx.utils import get_config_path

HOSTS = {
    "HQ": tuple({"addr": h[1], "port": h[2], "time": None, "site": h[0]} for h in hq_hosts + HQ_HOSTS),
    "EX": tuple({"addr": h[1], "port": h[2], "time": None, "site": h[0]} for h in EX_HOSTS),
    "GP": tuple({"addr": h[1], "port": h[2], "time": None, "site": h[0]} for h in GP_HOSTS),
}
# Backwards-compatible public name.  Values must not be mutated by callers.
hosts = HOSTS


def connect(proxy: dict) -> dict:
    """Measure a plain TCP connection and return a copied host record."""

    result = dict(proxy, time=None)
    started = time.perf_counter()
    try:
        with socket.create_connection((result["addr"], int(result["port"])), timeout=0.7):
            result["time"] = (time.perf_counter() - started) * 1000
    except OSError as exc:
        logger.debug("%s:%s 验证失败: %s", result["addr"], result["port"], exc)
    return result


def connect2(proxy: dict, index: str = "HQ") -> dict:
    """Validate a host using the corresponding TDX protocol."""

    if index == "GP":
        return connect(proxy)

    result = dict(proxy, time=None)
    api = TdxHq_API() if index == "HQ" else TdxExHq_API()
    try:
        with api.connect(result["addr"], int(result["port"]), time_out=0.7):
            started = time.perf_counter()
            if index == "HQ":
                healthy = api.get_security_bars(9, 1, "600000", 0, 1)
            else:
                healthy = api.get_instrument_count()
            if healthy:
                result["time"] = (time.perf_counter() - started) * 1000
    except (OSError, RuntimeError, TypeError, ValueError, TdxConnectionError, TdxFunctionCallError) as exc:
        logger.debug("%s:%s 协议验证失败: %s", result["addr"], result["port"], exc)
    return result


def server(index: str | None = None, limit: int = 5, console: bool = False, sync: bool = True):
    """Return reachable servers ordered by response time.

    ``sync=False`` retains the historical API meaning of concurrent probing.
    Host templates are copied on every call, fixing the old one-shot behaviour
    where the global list was consumed by ``pop``.
    """

    if index not in HOSTS:
        raise ValueError(f"index 必须是 {', '.join(HOSTS)} 之一")
    candidates = [dict(item) for item in HOSTS[index]]

    if sync:
        checked = [connect(item) for item in candidates]
    else:
        workers = min(32, max(1, len(candidates)))
        with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="mootdx-server") as pool:
            checked = list(pool.map(lambda item: connect2(item, index), candidates))

    available = sorted((item for item in checked if item["time"] is not None), key=lambda item: item["time"])
    if limit and limit > 0:
        available = available[:limit]

    if console:
        from prettytable import PrettyTable

        table = PrettyTable(["Name", "Addr", "Port", "Time"])
        table.align = "l"
        for item in available:
            table.add_row([item["site"], item["addr"], item["port"], f"{item['time']:.2f} ms"])
        logger.info("\n%s", table)

    return [(item["addr"], int(item["port"])) for item in available]


def check_server(console: bool = False, limit: int = 5, sync: bool = False) -> None:
    bestip(console=console, limit=limit, sync=sync)


def bestip(console: bool = False, limit: int = 5, sync: bool = False) -> None:
    """Probe all server groups and atomically persist the fastest endpoints."""

    config_path = Path(get_config_path("config.json"))
    selected = copy.deepcopy(CONFIG)
    logger.info("选择响应最快的服务器...")

    for index in HOSTS:
        try:
            endpoints = server(index=index, limit=limit, console=console, sync=sync)
        except (OSError, RuntimeError, ValueError) as exc:
            logger.warning("%s 服务器测速失败: %s", index, exc)
            continue
        if endpoints:
            selected["BESTIP"][index] = endpoints[0]

    config_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = config_path.with_suffix(f"{config_path.suffix}.tmp")
    temporary.write_text(json.dumps(selected, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(config_path)


if __name__ == "__main__":
    bestip(sync=False, limit=5, console=True)
