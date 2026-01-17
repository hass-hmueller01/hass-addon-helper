#!/usr/bin/env python3
# ==============================================================================
# MQTT Config Parser
# This script reads MQTT broker configuration from a user-provided
# mqtt_config.py file and outputs the settings as environment variable exports.
# Holger Mueller - MIT License 2026
# v001 2026-01-17 hmueller01 Initial version
# ==============================================================================

import ast
import os

config_file = os.path.expanduser("~/.config/mqtt_config.py")

try:
    with open(config_file, "r") as f:
        tree = ast.parse(f.read(), filename=config_file)
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            key = node.targets[0].id
            value = ast.literal_eval(node.value)
            values[key] = value

    if "host" in values:
        print(f'export MQTT_HOST="{values["host"]}"')
    if "port" in values:
        print(f'export MQTT_PORT="{values["port"]}"')
    if "user" in values:
        print(f'export MQTT_USER="{values["user"]}"')
    if "pwd" in values:
        print(f'export MQTT_PASSWORD="{values["pwd"]}"')
except FileNotFoundError:
    print(f"# Config file {config_file} not found.")
