# geohello-uoa

A small reference package used in **GISCI 343, Week 9** for live coding.
It is the smallest example that exercises every concept in the lecture.

## What it covers

1. The minimum function inside a package (`hello`).
2. The bundled-data pattern (small CSV inside the package, found at runtime
   with `importlib.resources`).
3. The fetched-data pattern (Stats NZ Datafinder WFS, with on-disk caching).
4. A small set of pytest tests that confirm all of the above work.

## Folder layout

```
geohello/
├── pyproject.toml
├── README.md
├── .gitignore
├── src/
│   └── geohello/
│       ├── __init__.py            # public API
│       ├── core.py                # hello()
│       ├── loader.py              # load_sensors(), load_sa2_auckland()
│       ├── py.typed
│       └── data/
│           └── sensors.csv        # 5-row sample
└── tests/
    └── test_geohello.py
```

## Quick start

```bash
# 1. Initialise a virtual environment for this folder
uv venv

# 2. Install the package in editable mode with the geo extras
uv pip install -e ".[geo,dev]"

# 3. Run the tests
uv run pytest -v

# 4. Try the package interactively
uv run python -c "from geohello import hello, load_sensors; print(hello()); print(load_sensors())"
```

## Building the wheel

```bash
uv build
ls dist/
```

You should see two files.

```
dist/
├── geohello_uoa-0.1.0-py3-none-any.whl
└── geohello_uoa-0.1.0.tar.gz
```

To confirm that the bundled CSV is inside the wheel, unzip and look for it.

```bash
unzip -l dist/geohello_uoa-0.1.0-py3-none-any.whl | grep sensors.csv
```

## Stats NZ fetch (optional)

The `load_sa2_auckland` function downloads SA2 boundaries from the Stats NZ
Datafinder WFS endpoint and caches them in `~/.cache/geohello/`.

```bash
# Get an API key from https://datafinder.stats.govt.nz/
export STATS_NZ_API_KEY=4f1a...

uv run python -c "from geohello import load_sa2_auckland; print(load_sa2_auckland().shape)"
```

The first call hits the API. Every subsequent call reads from the local cache.

## Live-coding tips for the lecturer

This folder is the **finished state** of the live-coded demo. During the
lecture you can either show the files directly or build them up step by
step on screen and refer back to this folder for the exact snippets.

A natural progression:

1. Start with an empty folder and run `uv init --lib geohello`.
2. Replace `src/geohello/__init__.py` with a one-function `hello`. Run
   `uv build` and import it.
3. Add a `data/` folder with `sensors.csv`. Edit `loader.py` to use
   `importlib.resources`. Update `pyproject.toml` with the
   `[tool.hatch.build.targets.*]` blocks. Rebuild. `unzip -l` to verify.
4. Add `load_sa2_auckland` with lazy imports and the cache pattern.
   Show the API key handling without ever revealing your real key.
5. Add the test file and run `uv run pytest`.
