from flask import Blueprint


spark = Blueprint(
    "spark", __name__)


def page():
    return "Hello, spark!"


spark.add_url_rule(
    "/spark/page", view_func=page)


def get_blueprints():
    return [spark]
