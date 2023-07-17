#!/usr/bin/env python
import argparse
from contextlib import nullcontext
import json
import os
import requests
import ckanapi
from dotenv import load_dotenv
load_dotenv()

MY_API_KEY = os.getenv("API_KEY")
HEADERS = {
    'Authorization': MY_API_KEY
}
# If the package name exists, then this function will return the package ID as well as its resource's names and IDs 
def get_package_data(name):
    ckan = ckanapi.RemoteCKAN('http://data.buspark.io', apikey=MY_API_KEY)
    packages = ckan.action.current_package_list_with_resources()
    # print the package list and resources
    try:
        package_data = None
        resources = {}
        for package in packages:
            if package['name'] == name:
                package_data = package
                break
        if package_data is None:
            raise KeyError("Package does not exist")
        package_id = package_data['id']
        for resource in package_data['resources']:
            resources[resource['name']] = resource['id']
        return (package_id, resources)
    except KeyError as e:
        print(e)
def package_revise(package_id, resources, update_metafields, resource_updates):
    print(update_metafields)
    data_dict = {}
    data_dict['match'] = f'{{"id": "{package_id}"}}'
    if 'Remove' in update_metafields:
        removals = update_metafields['Remove']
        if len(removals) > 0:
            data_dict['filter'] = json.dumps(removals)
    if 'Update' in update_metafields:
        updates = update_metafields['Update']
        if len(updates) > 0:
            data_dict['update'] = json.dumps(updates)
    if len(resource_updates) > 0:
        for name, data in resource_updates.items():
            if name in resources:
                resource_id = resources[name]
                index = 'update__resources__'  + resource_id[0:6]
                data_dict[index] = json.dumps(data)
    print(data_dict)
    return data_dict
def dictionary(a):
    try:
        data = json.loads(a)
        return data
    except ValueError as e:
        print("Error: Please provide a json object in string format ")
        data = None
    return data
parser = argparse.ArgumentParser()
parser.add_argument("package_name", help="name of the package you want to update",
                    type=str)
#parser.add_argument("package", help="name of the package you want to update")
# {
#   "Update": {
#       "metafield1": "value1"
#   },
#   "Remove": [metafield1, metafield2,...]
# }
parser.add_argument("update_metafields", help="metafields that you want to update. \
                    See https://docs.ckan.org/en/2.10/api/index.html#module-ckan.logic.action.create for list of fields",
                    type=dictionary)
# Let's try to support resource patching right now (resource fields).
# {reosurce_name: [field to update, updated value], resource_name: field to update, updated value}
# Useful metafields: description, name
# Doesn't currently support deleting/adding a resource
parser.add_argument("resources", help="metafields that you want to clear. \
                    See https://docs.ckan.org/en/2.10/api/index.html#module-ckan.logic.action.create for list of fields",
                    type=dictionary)
 #parser.add_argument("remove_fields", help="metafields that you want to remove in a list format")
args = parser.parse_args()
package_name = args.package_name
update = args.update_metafields
resources = args.resources
print(resources)

#now we have the ID and the Resources
package_id, resource_list = get_package_data(package_name)
#insert the package_id and resource_list into our function
data_dict = package_revise(package_id, resource_list, update, resources)
#make API call
REVISE_URL = 'http://data.buspark.io/api/3/action/package_revise'          # API endpoint
response = requests.post(REVISE_URL, data=data_dict, headers=HEADERS)
response_dict = response.json()
print(response_dict)
