hass-addon-helper
=================

Lightweight helper utilities and a minimal runtime environment intended for
Python-based Home Assistant add-ons. The package is laid out using the
`src/`-layout and exposes a small API implemented in `src/addon/addon.py`.

Highlights
----------

- Minimal dependency footprint — only Python standard library is required at
	runtime.
- Includes an example demonstrating the addon behavior: `examples/addon_demo.py`.

Package layout
--------------

- `src/addon/addon.py` — the real implementation. It configures logging and
	loads MQTT connection information from `/data/options.json`, environment
	variables, or `~/.config/mqtt_config.py`. It exports the module-level
	symbols: `log`, `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`,
	`mqtt_host`, `mqtt_port`, `mqtt_user`, `mqtt_pwd`, `mqtt_ca_certs`, and
	`config`.
- `src/addon/__init__.py` — import wrapper to `src/addon/addon.py`
- `examples/addon_demo.py` — runnable demo showing the usage.

Quick start
-----------

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install development/test dependencies:

```bash
pip install -r requirements.txt
```

3. Run tests:

```bash
pytest -q
```

4. Try the addon demo from the project root:

```bash
python examples/addon_demo.py
```

Usage notes
-----------

```python
import addon
print(addon.mqtt_host)
addon.log.info("hello")
```

Contributing
------------

If you want to run or modify the addon's runtime behavior, edit
[src/addon/addon.py](src/addon/addon.py) and experiment with the demo
script. When making changes, keep side-effect free behavior in mind so the
package remains import-safe for tests and tooling.

License
-------

This project is licensed under the MIT License — see [LICENSE](./LICENSE) for details.
