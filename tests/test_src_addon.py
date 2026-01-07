"""
Tests for src/addon.py loading behavior.
"""
import importlib
import logging
import os
import sys


def _add_src_to_path():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src = os.path.join(root, "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    return src


def test_mqtt_attributes(monkeypatch):
    """Test access to mqtt attributes."""
    _add_src_to_path()
    # Provide environment so the implementation won't sys.exit()
    monkeypatch.setenv("MQTT_HOST", "test-host")
    monkeypatch.setenv("MQTT_PORT", "1883")
    monkeypatch.setenv("MQTT_USER", "user")
    monkeypatch.setenv("MQTT_PASSWORD", "pwd")

    addon = importlib.import_module("addon")
    assert addon.mqtt_host == "test-host"
    assert addon.mqtt_port == 1883
    assert addon.mqtt_user == "user"
    assert addon.mqtt_pwd == "pwd"
    # after access, the implementation module must be present
    assert "addon.addon" in sys.modules


def test_log_attributes(monkeypatch):
    """Test log level constants and log instance."""
    _add_src_to_path()
    monkeypatch.setenv("MQTT_HOST", "x")
    monkeypatch.setenv("MQTT_PORT", "1883")
    addon = importlib.import_module("addon")
    assert addon.DEBUG == logging.DEBUG
    assert addon.INFO == logging.INFO
    assert addon.WARNING == logging.WARNING
    assert addon.ERROR == logging.ERROR
    assert addon.CRITICAL == logging.CRITICAL
    assert isinstance(addon.log, logging.Logger)


def test_missing_attribute_raises(monkeypatch):
    """Accessing a missing attribute raises AttributeError."""
    _add_src_to_path()
    monkeypatch.setenv("MQTT_HOST", "x")
    monkeypatch.setenv("MQTT_PORT", "1883")
    addon = importlib.import_module("addon")
    try:
        getattr(addon, "this_attribute_does_not_exist")
        raise AssertionError("expected AttributeError")
    except AttributeError:
        pass
