"""Runtime configuration for mootdx.

Configuration is deliberately local and deterministic: importing the package or
creating a client never performs network discovery.  Users can still refresh the
fastest server explicitly with ``python -m mootdx bestip``.
"""

from __future__ import annotations

import copy
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from mootdx.consts import CONFIG
from mootdx.logger import logger
from mootdx.utils import get_config_path

__all__ = ["clone", "get", "has", "path", "set", "settings", "setup", "update"]

BASE = Path(__file__).resolve().parent.parent
CONF = Path(get_config_path("config.json"))

settings: dict[str, Any] = copy.deepcopy(CONFIG)
_loaded = False


def _merge(target: dict[str, Any], source: Mapping[str, Any]) -> None:
    """Recursively merge *source* into *target* without losing defaults."""

    for key, value in source.items():
        if isinstance(value, Mapping) and isinstance(target.get(key), dict):
            _merge(target[key], value)
        else:
            target[key] = copy.deepcopy(value)


def _write_default() -> None:
    CONF.parent.mkdir(parents=True, exist_ok=True)
    temporary = CONF.with_suffix(f"{CONF.suffix}.tmp")
    temporary.write_text(
        json.dumps(CONFIG, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(CONF)


def setup(*, force: bool = False) -> bool:
    """Load the user configuration and retain defaults for missing values.

    A missing file is initialized locally.  Invalid JSON is left untouched so a
    malformed user file is never silently destroyed.
    """

    global _loaded, settings
    if _loaded and not force:
        return True

    settings = copy.deepcopy(CONFIG)
    try:
        options = json.loads(CONF.read_text(encoding="utf-8"))
        if not isinstance(options, Mapping):
            raise ValueError("配置根节点必须是 JSON 对象")
        _merge(settings, options)
    except FileNotFoundError:
        logger.info("初始化配置文件: %s", CONF)
        _write_default()
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        logger.warning("忽略无效配置文件 %s: %s", CONF, exc)

    _loaded = True
    return True


def has(key: str, value: object) -> bool:
    container = get(key)
    try:
        return value in container
    except TypeError:
        return False


def set(key: str, value: Any) -> None:  # noqa: A001 - compatibility API
    """Set a configuration value.

    Dotted keys are supported.  Mapping values are merged to preserve sibling
    settings, matching how server overrides are commonly supplied.
    """

    parts = key.split(".")
    target = settings
    for part in parts[:-1]:
        target = target.setdefault(part, {})

    leaf = parts[-1]
    if isinstance(value, Mapping) and isinstance(target.get(leaf), dict):
        _merge(target[leaf], value)
    else:
        target[leaf] = copy.deepcopy(value)


def get(key: str, default: Any = None) -> Any:
    current: Any = settings
    for part in key.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return default
        current = current[part]
    return current


def path(key: str, value: str | Path | None = None) -> Path:
    configured = Path(get(key, ""))
    result = configured if configured.is_absolute() else BASE / configured
    return result / value if value is not None else result


def clone() -> dict[str, Any]:
    return copy.deepcopy(settings)


def update(options: Mapping[str, Any]) -> None:
    _merge(settings, options)
