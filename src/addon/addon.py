"""
Minimal addon environment for Python inspired by bashio.

Module providing bashio like logging output, e.g.: log.info("service starting ...")
[2025-01-01 18:29:31] INFO: service starting ...

Loads MQTT configuration from /data/options.json, environment variables, or ~/.config/mqtt_config.py
as mqtt_host, mqtt_port, mqtt_user, mqtt_pwd, mqtt_ca_certs.

Proivides `config` dictionary with all options from /data/options.json if available.

MIT License
Copyright (c) 2025-2026 Holger Mueller

v0.1.0 2025-12-27 Initial revision
v0.2.0 2026-01-06 Migrated to python-addon-helper structure
"""
from __future__ import annotations
import logging
import json
import os
import sys
import importlib.util
from typing import Any


def _setup_root_logger(name: str | None = None) -> logging.Logger:
    """Setup the root logger with a StreamHandler and formatter."""
    root = logging.getLogger(name)
    if not root.handlers:
        handler = logging.StreamHandler(stream=sys.stdout)
        # default format can be overridden by environment
        fmt = os.getenv("BASHIO_LOG_FORMAT", "[%(asctime)s] %(levelname)s: %(message)s")
        datefmt = os.getenv("BASHIO_LOG_DATEFMT", "%Y-%m-%d %H:%M:%S")
        formatter = logging.Formatter(fmt, datefmt=datefmt)
        handler.setFormatter(formatter)
        root.addHandler(handler)
    # default level can be overridden by environment
    level_name = os.getenv("BASHIO_LOG_LEVEL", "INFO").upper()
    try:
        root.setLevel(getattr(logging, level_name))
    except Exception:  # pylint: disable=broad-except
        root.setLevel(logging.INFO)
    return root


def _setup_config() -> dict[str, Any]:
    """Setup logging configuration from environment variables."""
    global mqtt_host, mqtt_port, mqtt_user, mqtt_pwd, mqtt_ca_certs  # pylint: disable=global-statement
    _config: dict[str, Any] = {}
    homeassistant_options: str = "/data/options.json"
    if os.path.exists(homeassistant_options):
        with open(homeassistant_options, "r", encoding="utf-8") as f:
            _config = json.load(f)
        if "mqtt_host" in _config and "mqtt_port" in _config:
            mqtt_host = _config.get("mqtt_host")
            mqtt_port = _config.get("mqtt_port", 1883)
            mqtt_user = _config.get("mqtt_user", "")
            mqtt_pwd = _config.get("mqtt_password", "")
            mqtt_ca_certs = _config.get("mqtt_ca_certs", "") # do not use with port 1883
            log.info("Using configured MQTT Host: %s:%s", mqtt_host, mqtt_port)
        elif "mqtt" in _config:
            mqtt_cfg = _config["mqtt"]
            mqtt_host = mqtt_cfg.get("host")
            mqtt_port = mqtt_cfg.get("port")
            mqtt_user = mqtt_cfg.get("username", "")
            mqtt_pwd = mqtt_cfg.get("password", "")
            mqtt_ca_certs = ""  # not supported in Home Assistant internal MQTT
            log.info("Using internal MQTT Host: %s:%s", mqtt_host, mqtt_port)
        else:
            log.error("No MQTT broker configured and no internal MQTT service available.")
            sys.exit(1)
    else:
        log.warning("Home Assistant configuration file not found: %s", homeassistant_options)
        mqtt_host = os.getenv('MQTT_HOST', "")
        mqtt_port = int(os.getenv("MQTT_PORT", "1883"))
        mqtt_user = os.getenv("MQTT_USER", "")
        mqtt_pwd = os.getenv("MQTT_PASSWORD", "")
        mqtt_ca_certs = os.getenv("MQTT_CA_CERTS", "")  # not used with port 1883
        if mqtt_host != "":
            log.info("Using environment configured MQTT Host: %s:%s", mqtt_host, mqtt_port)
        else:
            log.warning("No environment variables found: MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD")
            mqtt_config_file_path = os.path.join(os.getenv('HOME', ""), ".config", "mqtt_config.py")
            mqtt_config_spec = importlib.util.spec_from_file_location("mqtt_config", mqtt_config_file_path)
            if os.path.exists(mqtt_config_file_path) and mqtt_config_spec is not None and mqtt_config_spec.loader is not None:
                mqtt_config = importlib.util.module_from_spec(mqtt_config_spec)
                mqtt_config_spec.loader.exec_module(mqtt_config)
                mqtt_host = mqtt_config.host
                mqtt_port = mqtt_config.port
                mqtt_user = mqtt_config.user
                mqtt_pwd = mqtt_config.pwd
                mqtt_ca_certs = mqtt_config.ca_certs
                log.info("Using mqtt_config.py configured MQTT Host: %s:%s", mqtt_host, mqtt_port)
            else:
                log.error("Could not load ~/.config/mqtt_config.py to get MQTT broker configuration. Exiting.")
                sys.exit(1)
    return _config


# provide logging level constants so callers can use them like `logging.DEBUG`
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

# export a named logger for consumers of this module
log = _setup_root_logger("hass-addon")

# export configuration dictionary and MQTT connection parameters
mqtt_host, mqtt_port, mqtt_user, mqtt_pwd, mqtt_ca_certs = "", 0, "", "", ""
config = _setup_config()
