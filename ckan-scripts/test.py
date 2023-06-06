import ckanapi
import json
import os
MY_API_KEY = os.getenv("API_KEY")
HEADERS = {
    'Authorization': MY_API_KEY
}
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
                index = 'resource' + '__' + resource_id
                data_dict[index] = f'{data}'
    print(data_dict)
    return data_dict
def get_package_data(name):
    ckan = ckanapi.RemoteCKAN('http://data.buspark.io', apikey=MY_API_KEY)
    packages = ckan.action.current_package_list_with_resources()
    # print the package list and resources
    try:
        package_data = None
        resources = {}
        for package in packages:
            print(package['name'])
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

rr = {
    "parcel" : "id_123_456"
}
r={}
a = '{"IBB-Holdings":{"title":"ibb-holdings"}}' #same input from terminal
b = (json.loads(a))
print(b)
print(package_revise("123456", rr, b, r))
