"""Data loaders, demonstrating the two patterns from the lecture.

Pattern 1: bundled data, found at runtime with ``importlib.resources``.
Pattern 2: fetched data, downloaded from Stats NZ via WFS and cached.

The optional dependencies ``geopandas`` and ``requests`` are imported
lazily inside :func:`load_sa2_auckland` so that the bundled-data
function still works for users who installed only the core package.
"""

from __future__ import annotations

import os
from importlib import resources
from io import BytesIO
from pathlib import Path

import pandas as pd

# Stats NZ Datafinder layer ID for SA2 2023 generalised polygons.
SA2_LAYER = "layer-111228"

# Templated WFS endpoint, key is injected at call time.
WFS_URL = "https://datafinder.stats.govt.nz/services;key={key}/wfs"

# Per-user cache directory, hidden in the home folder.
CACHE_DIR = Path.home() / ".cache" / "geohello"

# Auckland CBD bounding box in NZTM (EPSG:2193).
DEFAULT_BBOX = "1740000,5900000,1790000,5950000,EPSG:2193"


def _data_path(filename: str) -> str:
    """Resolve a path to a bundled data file.

    Using ``importlib.resources`` rather than a hard-coded path makes
    this work whether the package is installed from PyPI, from a wheel,
    or in editable mode.
    """
    ref = resources.files("geohello") / "data" / filename
    return str(ref)


def load_sensors() -> pd.DataFrame:
    """Load the bundled sample sensor table.

    Returns
    -------
    pandas.DataFrame
        A small sample of Auckland CBD pedestrian sensor metadata
        (sensor id, address, latitude, longitude). Five rows.
    """
    return pd.read_csv(_data_path("sensors.csv"))


def _get_api_key() -> str:
    """Read the Stats NZ API key from the environment.

    Raises
    ------
    EnvironmentError
        If ``STATS_NZ_API_KEY`` is not set.
    """
    key = os.getenv("STATS_NZ_API_KEY")
    if key is None:
        raise EnvironmentError(
            "Set STATS_NZ_API_KEY in your environment "
            "or .env file before calling this function."
        )
    return key


def load_sa2_auckland(api_key: str | None = None, use_cache: bool = True):
    """Download Auckland CBD SA2 boundaries from Stats NZ.

    Lazy-imports ``geopandas`` and ``requests`` so the rest of the
    package does not require the ``geo`` extra.

    Parameters
    ----------
    api_key : str, optional
        Stats NZ Datafinder API key. If ``None``, the function reads
        the ``STATS_NZ_API_KEY`` environment variable.
    use_cache : bool, default True
        If True, cache the result locally under ``~/.cache/geohello/``
        and read from there on subsequent calls.

    Returns
    -------
    geopandas.GeoDataFrame
        SA2 polygons for the Auckland CBD bounding box, in EPSG:2193.
    """
    # Lazy import keeps the core install lightweight.
    import geopandas as gpd
    import requests

    api_key = api_key or _get_api_key()

    cache_file = CACHE_DIR / "sa2_auckland.gpkg"
    if use_cache and cache_file.exists():
        return gpd.read_file(cache_file)

    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeNames": SA2_LAYER,
        "outputFormat": "json",
        "srsName": "EPSG:2193",
        "bbox": DEFAULT_BBOX,
    }
    response = requests.get(
        WFS_URL.format(key=api_key),
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    gdf = gpd.read_file(BytesIO(response.content))

    if use_cache:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        gdf.to_file(cache_file, driver="GPKG")

    return gdf
