import ckanapi
import requests
import sys
import os
import json 
from dotenv import load_dotenv

load_dotenv()
my_API_KEY = os.getenv("API_KEY")

#!/usr/bin/python3
token = my_API_KEY
selected_id = 'd874af6c-cd54-4c4a-a05d-504df04e1df2'
#id, name, title, notes, url, version, author, author_email, maintainer, maintainer_email, license_id, private, owner_org, state, type, resources, tags, groups, extras
# put the details of the dataset we're going to create into a dict
data_dict = {
    'match': f'{{"id": "{selected_id}"}}',
    'update': '{"notes": "Collecting a record of items of personal property, such as equipment and supplies, for which state agencies no longer have a business use, but that have some reuse value. ","title": "state_surplus"}'
}

# use the json module to dump the dictionary to a string for posting, encoding the URL
# creating a dataset requires an authorization header
headers = {
    'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJjV1c2WUcwQmJNYXYyanE1clBQeEZjVWZNRjB2emVmTWF1a19laUZ4bDJjIiwiaWF0IjoxNjc3ODI2NzAyfQ.7ivzMXrnyDsjFa9ZF6QMI73TqpAZgYoaxFzIZQlXj7I',
    #'Content-Type': 'multipart/form-data'
}
# we'll use the package_create function to create a new dataset.
url = 'http://data.buspark.io/api/3/action/package_revise'
# making HTTP request 
response = requests.post(url, data=data_dict, headers=headers)

# use the json module to load CKAN's response into a dictionary
response_dict = response.json()
print(response_dict)


