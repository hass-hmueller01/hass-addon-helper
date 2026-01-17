# Makefile for hass-addon-helper install process
#
# MIT License
# Copyright (c) 2026 Holger Mueller
#
# Changelog:
# - 2026-01-07: Initial revision (hmueller)
# - 2026-01-17: Added py- targets for python package management (hmueller)

.PHONY: all install py-install py-uninstall py-upgrade py-test py-examples

all: install

install:
	@echo "This is a helper Makefile to install the hass-addon-helper."
	copy -a ./bin/* /usr/local/bin/

py-install:
	@echo "This is a helper Makefile to install the hass-addon-helper."
	pip install .

py-uninstall:
	pip uninstall -y hass-addon-helper

py-upgrade:
	pip install --upgrade hass-addon-helper

py-test:
	pip install -q pytest
	pytest -v tests

py-examples:
	python examples/addon_demo.py
