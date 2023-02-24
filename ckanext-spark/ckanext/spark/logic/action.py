import ckan.plugins.toolkit as tk
import ckanext.spark.logic.schema as schema


@tk.side_effect_free
def spark_get_sum(context, data_dict):
    tk.check_access(
        "spark_get_sum", context, data_dict)
    data, errors = tk.navl_validate(
        data_dict, schema.spark_get_sum(), context)

    if errors:
        raise tk.ValidationError(errors)

    return {
        "left": data["left"],
        "right": data["right"],
        "sum": data["left"] + data["right"]
    }


def get_actions():
    return {
        'spark_get_sum': spark_get_sum,
    }
