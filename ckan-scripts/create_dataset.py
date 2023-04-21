import ckanapi
import requests
import sys
import os
import json
from dotenv import load_dotenv
load_dotenv()

MY_API_KEY = os.getenv("API_KEY")

dsCreator = 'riskEvaluator.json'
#read JSON file 

f = open(os.path.join(sys.path[0],'jsonf',dsCreator))
data = json.load(f) #converts json object to python dict

package_name = data['projectName']
package_ds = data['description']
package_src_url = data['url']
package_rf = data['resourceFolder']
package_org = data['owner_org']

ckan = ckanapi.RemoteCKAN('http://data.buspark.io', apikey=MY_API_KEY)

# This follows the example provided in ckanapi repo: Create the "Sample" dataset.
try:
    print('Creating {package_title}')
    package = ckan.action.package_create(name=package_name, notes=package_ds, url = package_src_url, owner_org=package_org)
except ckanapi.ValidationError as e:
    if (e.error_dict['__type'] == 'Validation Error' and
       e.error_dict['name'] == ['That URL is already in use.']):
        print('"{package_title}" package already exists'.format(**locals()))
        package = ckan.action.package_show(id=package_name)
        print(package)
    else:
        raise

for filename in os.listdir(os.path.join(sys.path[0],package_rf)):
    csv_file = open(os.path.join(sys.path[0],package_rf,filename), "rb")
    path = os.path.join(sys.path[0],package_rf,filename)
    extension = os.path.splitext(filename)[1][1:].upper()
    resource_name = filename[0:-4] #remove extension from resource name
    print('Creating "{resource_name}" resource'.format(**locals()))
    r = requests.post('http://data.buspark.io/api/3/action/resource_create',
                      data={'package_id': package['id'],
                            'name': resource_name,
                            'format': extension,
                            'url': 'upload',  # Needed to pass validation
                            },
                      headers={'Authorization': MY_API_KEY},
                      files={"upload": csv_file})
    print(r)
    print(r.json())
    if r.status_code != 200:
        print('Error while creating resource: {0}'.format(r.content))
        break
