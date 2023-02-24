import ckan.plugins.toolkit as tk


@tk.auth_allow_anonymous_access
def spark_get_sum(context, data_dict):
    return {"success": True}


def get_auth_functions():
    return {
        "spark_get_sum": spark_get_sum,
    }
