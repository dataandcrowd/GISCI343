"""Tests for the geohello live-coding example."""

from __future__ import annotations

import pandas as pd

from geohello import hello, load_sensors


# -- core.hello --------------------------------------------------------

def test_hello_default():
    assert "Auckland" in hello()


def test_hello_custom_place():
    assert hello("Tokyo") == "Hello from Tokyo!"


def test_hello_returns_string():
    assert isinstance(hello(), str)


# -- loader.load_sensors (bundled data) --------------------------------

def test_load_sensors_returns_dataframe():
    df = load_sensors()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_load_sensors_has_required_columns():
    df = load_sensors()
    required = {"sensor_id", "address", "latitude", "longitude"}
    assert required.issubset(df.columns)


def test_load_sensors_returns_five_rows():
    df = load_sensors()
    assert len(df) == 5
