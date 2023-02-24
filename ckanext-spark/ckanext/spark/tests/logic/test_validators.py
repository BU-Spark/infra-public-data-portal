"""Tests for validators.py."""

import pytest

import ckan.plugins.toolkit as tk

from ckanext.spark.logic import validators


def test_spark_reauired_with_valid_value():
    assert validators.spark_required("value") == "value"


def test_spark_reauired_with_invalid_value():
    with pytest.raises(tk.Invalid):
        validators.spark_required(None)
