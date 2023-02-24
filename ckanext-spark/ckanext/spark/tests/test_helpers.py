"""Tests for helpers.py."""

import ckanext.spark.helpers as helpers


def test_spark_hello():
    assert helpers.spark_hello() == "Hello, spark!"
