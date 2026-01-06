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


def test_import_package_does_not_load_submodule():
    _add_src_to_path()
    addon = importlib.import_module("addon")
    # package import should not immediately load the implementation module
    assert "addon.addon" not in sys.modules


def test_attribute_access_triggers_module_load(monkeypatch):
    _add_src_to_path()
    # Provide environment so the implementation won't sys.exit()
    monkeypatch.setenv("MQTT_HOST", "test-host")
    monkeypatch.setenv("MQTT_PORT", "1883")
    monkeypatch.setenv("MQTT_USER", "user")
    monkeypatch.setenv("MQTT_PASSWORD", "pwd")

    addon = importlib.import_module("addon")
    # Accessing attributes triggers lazy load
    assert addon.mqtt_host == "test-host"
    assert addon.mqtt_port == 1883
    assert addon.mqtt_user == "user"
    assert addon.mqtt_pwd == "pwd"
    assert isinstance(addon.log, logging.Logger)
    # after access, the implementation module must be present
    assert "addon.addon" in sys.modules


def test_missing_attribute_raises(monkeypatch):
    _add_src_to_path()
    monkeypatch.setenv("MQTT_HOST", "x")
    monkeypatch.setenv("MQTT_PORT", "1883")
    addon = importlib.import_module("addon")
    try:
        getattr(addon, "this_attribute_does_not_exist")
        raise AssertionError("expected AttributeError")
    except AttributeError:
        pass
