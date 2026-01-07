"""
Demonstration of behavior for the package.

Usage:
    python examples/addon_demo.py

MIT License
Copyright (c) 2025-2026 Holger Mueller
"""
# pylint: disable=logging-fstring-interpolation, wrong-import-position, broad-except
import os
import sys

# Make the 'src' directory importable so the 'addon' package can be found.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
sys.path.insert(0, SRC)
print("sys.path[0] ->", sys.path[0])

import addon

try:
    print("\nAccessing addon attributes:")
    addon.log.info(f"This is a test log.info() message from {os.path.basename(__file__)}")
    addon.log.info(f"MQTT Host: {addon.mqtt_host}")
    addon.log.info(f"MQTT Port: {addon.mqtt_port}")

    print("\nTesting log levels:")
    print("Log level DEBUG:")
    addon.log.debug("Debug log level reached before setting level to DEBUG.")
    addon.log.setLevel(addon.DEBUG)
    addon.log.debug("Debug log level reached after setting level to DEBUG.")
    print("Log level ERROR:")
    addon.log.error("Error log level reached.")
    print("Log level WARNING:")
    addon.log.warning("Warning log level reached.")
    print("Log level CRITICAL:")
    addon.log.critical("Critical log level reached.")
except Exception as exc:
    print("Access raised:", type(exc).__name__, exc)
