# Makefile for hass-addon-helper install process
#
# MIT License
# Copyright (c) 2026 Holger Mueller
#
# Changelog:
# - 2026-01-07: Initial revision (hmueller)

.PHONY: all install uninstall upgrade test examples

all: test install

install:
	@echo "This is a helper Makefile to install the hass-addon-helper."
	pip install .

uninstall:
	pip uninstall -y hass-addon-helper

upgrade:
	pip install --upgrade hass-addon-helper

test:
	pip install -q pytest
	pytest -v tests

examples:
	python examples/addon_demo.py
