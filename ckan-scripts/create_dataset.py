import ckanapi
import requests
import sys
import os
import json

MY_API_KEY = os.getenv("API_KEY")

dsCreator = 'riskEvaluator.json'

f = open(dsCreator)
data = json.load(f)

package_name = data['project_name']
package_ds = data['description']
package_more_information = data['more_information']
package_uris = data['uris']
package_org = data['owner_org']

ckan = ckanapi.RemoteCKAN('http://data.buspark.io', apikey=MY_API_KEY)

try:
    print(f'Creating {package_name}')
    package = ckan.action.package_create(name=package_name, notes=package_ds, url = package_more_information, owner_org=package_org)
except ckanapi.ValidationError as e:
    if e.error_dict.get('__type') == 'Validation Error':
        if 'name' in e.error_dict and e.error_dict['name'] == ['That URL is already in use.']:
            print(f'"{package_name}" package already exists')
            package = ckan.action.package_show(id=package_name)
            print(package)
        elif 'owner_org' in e.error_dict:
            print(f"Error: {e.error_dict['owner_org'][0]}")
            sys.exit(1)  # Exit the script if 'owner_org' validation error occurs
        else:
            print(f'Error: {e}')
    else:
        print(f'Error: {e}')
else:
    print('Package created successfully')

for filename in os.listdir(os.path.join(sys.path[0],package_uris)):
    csv_file = open(os.path.join(sys.path[0],package_uris,filename), "rb")
    path = os.path.join(sys.path[0],package_uris,filename)
    extension = os.path.splitext(filename)[1][1:].upper()
    resource_name = filename[0:-4] 
    print('Creating "{resource_name}" resource'.format(**locals()))
    r = requests.post('http://data.buspark.io/api/3/action/resource_create',
                      data={'package_id': package['name'],
                            'name': resource_name,
                            'format': extension,
                            'url': 'upload',  
                            },
                      headers={'Authorization': MY_API_KEY},
                      files={"upload": csv_file})
    print(r)
    print(r.json())
    if r.status_code != 200:
        print('Error while creating resource: {0}'.format(r.content))
        break
