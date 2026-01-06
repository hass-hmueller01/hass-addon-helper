"""
Demonstration of lazy import behavior for the package.

Run this script from the project root to see that importing the package
does not immediately load ``src/addon/addon.py``; attribute access triggers
the actual import.

Usage:
    python examples/lazy_import_demo.py
"""
import os
import sys

# Make the 'src' directory importable so the 'addon' package can be found.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
sys.path.insert(0, SRC)
print("sys.path[0] ->", sys.path[0])

print("Importing package 'addon' (package-level init only)...")
import addon  # this imports the package but should NOT execute src/addon/addon.py yet

print("Is submodule 'addon.addon' loaded?", "addon.addon" in sys.modules)

print("Accessing 'addon.log' to trigger real module import (or error)...")
try:
    #_ = addon.log
    addon.log.info("This is a test log message from lazy_import_demo.py")
    addon.log.error(f"MQTT Host: {addon.mqtt_host}")
    addon.log.warning(f"MQTT Port: {addon.mqtt_port}")
    print("After access: 'addon.addon' loaded?", "addon.addon" in sys.modules)
except Exception as exc:  # pylint: disable=broad-except
    print("Access raised:", type(exc).__name__, exc)
