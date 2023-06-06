import argparse
import json
import os
import requests
from dotenv import load_dotenv
import ckanapi
load_dotenv()

"""
Description of the file/module.
Notes: resources that aren't mentioned should be removed (not purged!)
Args:
    arg1 (string): name of the package
    arg2 (dict): metafields that you want to update/remove in this format: '{"Update":{"notes":"modifyingstuff"}, "Remove":{"title"}}'
    arg3 (dict): resources and metafields that you want to update in this format: '{"resource_1":{"name":"new_name"}}
Returns:
    type: Description of the return value(s).
Example:
    python3 test.py "risk_evaluator" '{"Update":{"notes":"modifyingstuff"}}' '{}'
"""

MY_API_KEY = os.getenv("API_KEY")
HEADERS = {
    'Authorization': MY_API_KEY
}

def get_package_data(name):
    """Return the id and a dictionary of resources and their ids by traversing the site.
    
    Args:
        name: name of the package
    """
    ckan = ckanapi.RemoteCKAN('http://data.buspark.io', apikey=MY_API_KEY)
    packages = ckan.action.current_package_list_with_resources()
    
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
    """Attempts to create a data dictionary to pass into package_revise CKAN API call.
    
    Args:
        package_id: id of the package (string)
        resources: the package's resources (dict)
        update_metafields: metafields to be updated or removed (dict)
        resource_updates: resources and resource metafields to be removed (dict)
    """
    #print(update_metafields) debugging
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
    """Validates user input, returns error if input is invalid json string format
    
    Args:
        a: user input in json string format
    """
    try:
        data = json.loads(a)
        return data
    except ValueError as e:
        print("Error: Please provide a json object in string format ")
        data = None
    
    return data


parser = argparse.ArgumentParser()
parser.add_argument(
    "package_name",
    help="name of the package you want to update",
    type=str
)

parser.add_argument(
    "update_metafields",
    help="metafields that you want to update. See https://docs.ckan.org/en/2.10/api/index.html#module-ckan.logic.action.create for list of fields",
    type=dictionary
)

parser.add_argument(
    "resources",
    help="metafields that you want to clear. See https://docs.ckan.org/en/2.10/api/index.html#module-ckan.logic.action.create for list of fields",
    type=dictionary
)

args = parser.parse_args()

# Grabbing user inputs

package_name = args.package_name
update = args.update_metafields
resources = args.resources
print(resources)

package_id, resource_list = get_package_data(package_name)
data_dict = package_revise(package_id, resource_list, update, resources)
REVISE_URL = 'http://data.buspark.io/api/3/action/package_revise'
response = requests.post(REVISE_URL, data=data_dict, headers=HEADERS)
response_dict = response.json()
json_pretty = json.dumps(response_dict, indent=2)
print(json_pretty)
#pretty printing - built in python function
