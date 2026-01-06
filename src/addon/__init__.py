"""Package initializer for the addon helpers.

This module provides a lazy import wrapper for ``.addon`` so importing the
package does not immediately execute the addon's top-level initialization
logic (which may call ``sys.exit()`` when configuration is missing).

Attributes from the real module are loaded on first access via ``__getattr__``.
"""
from __future__ import annotations

from typing import Any
import importlib

__all__ = [
    "log",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
    "mqtt_host",
    "mqtt_port",
    "mqtt_user",
    "mqtt_pwd",
    "mqtt_ca_certs",
    "config",
]

__version__ = "0.1.0"

_MODULE: Any | Exception | None = None


def _load_module() -> Any:
    global _MODULE
    if _MODULE is None:
        try:
            _MODULE = importlib.import_module(".addon", __name__)
        except Exception as exc:  # store exception to raise on attribute access
            _MODULE = exc
    return _MODULE


def __getattr__(name: str) -> Any:  # type: ignore
    """Lazily load attributes from the real ``addon`` module.

    If loading the module failed, raise an informative ImportError chaining
    the original error.
    """
    mod = _load_module()
    if isinstance(mod, Exception):
        raise ImportError(
            "Failed to import the local addon module; ensure src/addon/addon.py is present and importable"
        ) from mod
    try:
        return getattr(mod, name)
    except AttributeError as exc:
        raise AttributeError(f"module 'addon' has no attribute '{name}'") from exc


def __dir__() -> list[str]:
    # Merge declared public API with attributes from the underlying module if available
    names = list(__all__)
    mod = _load_module()
    if not isinstance(mod, Exception):
        names.extend([n for n in dir(mod) if not n.startswith("__")])
    return sorted(set(names))
