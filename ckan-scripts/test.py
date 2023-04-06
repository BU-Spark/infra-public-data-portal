import argparse
import json
def dict_checker(a):
    try: 
        json.loads(a)
    except ValueError as e:
        raise argparse.ArgumentTypeError("input must be json object surrounded by single quotes") from e
parser = argparse.ArgumentParser()
#parser.add_argument("package", help="name of the package you want to update")
parser.add_argument("update_metafields", help="metafields that you want to update. See https://docs.ckan.org/en/2.10/api/index.html#module-ckan.logic.action.create for list of fields", type=dict_checker)
#parser.add_argument("remove_fields", help="metafields that you want to remove in a list format")
args = parser.parse_args()
input = args.update_metafields
toprint = json.loads(input)
print(type(toprint))
