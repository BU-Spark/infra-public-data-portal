import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv()
my_API_KEY = os.getenv("API_KEY")
package_id = 'd874af6c-cd54-4c4a-a05d-504df04e1df2'
APIKEY = my_API_KEY
#this code does not iterate over json files right now 
#read JSON file 
for filename in os.listdir(os.path.join(sys.path[0],'StateSurplusS21')):
    csv_file = open(os.path.join(sys.path[0],'StateSurplusS21',filename), "rb")
    path = os.path.join(sys.path[0],'StateSurplusS21',filename)
    extension = os.path.splitext(filename)[1][1:].upper()
    resource_name = filename[0:-4] #remove extension from resource name
    print('Creating "{resource_name}" resource'.format(**locals()))
    r = requests.post('http://data.buspark.io/api/3/action/resource_create',
                      data={'package_id': package_id,
                            'name': resource_name,
                            'format': extension,
                            'url': 'upload',  # Needed to pass validation
                            },
                      headers={'Authorization': APIKEY},
                      files={"upload": csv_file})
    print(r.status_code)
    print(r.text)
    print(r)
