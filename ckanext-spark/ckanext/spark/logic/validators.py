import ckan.plugins.toolkit as tk


def spark_required(value):
    if not value or value is tk.missing:
        raise tk.Invalid(tk._("Required"))
    return value


def get_validators():
    return {
        "spark_required": spark_required,
    }
