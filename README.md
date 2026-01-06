python-addon-helper
===================

Lightweight helper utilities and a minimal runtime environment intended for
Python-based Home Assistant add-ons. The package is laid out using the
`src/`-layout and exposes a small API implemented in `src/addon/addon.py`.

Highlights
----------

- Minimal dependency footprint — only Python standard library is required at
	runtime.
- A package-level lazy-import wrapper prevents side effects when importing the
	package (useful for tests and tooling). See `src/addon/__init__.py`.
- Includes an example demonstrating the lazy-import behavior: `examples/lazy_import_demo.py`.

Package layout
--------------

- `src/addon/addon.py` — the real implementation. It configures logging and
	loads MQTT connection information from `/data/options.json`, environment
	variables, or `~/.config/mqtt_config.py`. It exports the module-level
	symbols: `log`, `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`,
	`mqtt_host`, `mqtt_port`, `mqtt_user`, `mqtt_pwd`, `mqtt_ca_certs`, and
	`config`.
- `src/addon/__init__.py` — lazy import wrapper that defers importing
	`src/addon/addon.py` until an attribute is accessed. This avoids running
	top-level initialization (which may call `sys.exit()`) on a simple
	`import addon`.
- `examples/lazy_import_demo.py` — runnable demo showing when the real
	submodule is loaded.

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

4. Try the lazy-import demo from the project root:

```bash
python examples/lazy_import_demo.py
```

Usage notes
-----------

- Importing the package `addon` does not immediately load the implementation
	in `src/addon/addon.py`. This allows code that inspects or imports the
	package (for example, documentation tools or unit tests) to avoid running
	configuration-dependent startup logic.
- To access the real runtime objects, just use the attribute as usual:

```python
import addon
print(addon.mqtt_host)
addon.log.info("hello")
```

If `src/addon/addon.py` cannot be imported (missing file or import error),
the package will raise an informative `ImportError` on attribute access.

Contributing
------------

If you want to run or modify the addon's runtime behavior, edit
[src/addon/addon.py](src/addon/addon.py#L1-L200) and experiment with the demo
script. When making changes, keep side-effect free behavior in mind so the
package remains import-safe for tests and tooling.

License
-------

This project is licensed under the MIT License — see [LICENSE](./LICENSE) for details.
