import os
import requests
from dotenv import load_dotenv
load_dotenv()

MY_API_KEY = os.getenv("API_KEY")
HEADERS = {
    'Authorization': MY_API_KEY
}
PACKAGE_ID = 'd874af6c-cd54-4c4a-a05d-504df04e1df2'                 # In the future we would like to pass package ID or name as a parameter 
URL = 'http://data.buspark.io/api/3/action/package_revise'          # API endpoint
# id, name, title, notes, url, version, author, author_email, maintainer,
#  maintainer_email, license_id, private, owner_org, state, type, resources, tags, groups, extras
# put the details of the dataset we're going to create into a dict
data_dict = {
    'match': f'{{"id": "{PACKAGE_ID}"}}',
    'update': '{"notes": "Collecting a record of items of personal property, \
                          such as equipment and supplies, for which state agencies \
                          no longer have a business use, but that have some reuse value. ",\
                "title": "state_surplus"\
                }',
        'update__resources__dfaf6f' : '{"name": "parcel-geoData"}'

}
# use the json module to dump the dictionary to a string for posting, encoding the URL
# creating a dataset requires an authorization header
# we'll use the package_create function to create a new dataset.
# making HTTP request 
response = requests.post(URL, data=data_dict, headers=HEADERS)
# use the json module to load CKAN's response into a dictionary
response_dict = response.json()
print(response_dict)