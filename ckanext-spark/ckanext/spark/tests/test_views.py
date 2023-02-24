"""Tests for views.py."""

import pytest

import ckanext.spark.validators as validators


import ckan.plugins.toolkit as tk


@pytest.mark.ckan_config("ckan.plugins", "spark")
@pytest.mark.usefixtures("with_plugins")
def test_spark_blueprint(app, reset_db):
    resp = app.get(tk.h.url_for("spark.page"))
    assert resp.status_code == 200
    assert resp.body == "Hello, spark!"
