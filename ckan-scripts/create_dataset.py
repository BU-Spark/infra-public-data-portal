#!/usr/bin/env python

"""
The purpose of this script is to take in the json file produced by compile_json.py and upload all of the projects to our 
Data@Spark website.

Again, only works for data stored in GitHub repos, as it depends on the raw.githubusercontent links for the data
"""
import ckanapi
import requests
import sys
import os
import json
from io import BytesIO

# env variable in the future
MY_API_KEY = os.getenv("API_KEY")

all_projects = 'spark_datasets_2023-08-10.json'

with open(all_projects) as f:
    data = json.load(f)

ckan = ckanapi.RemoteCKAN('http://data.buspark.io', apikey=MY_API_KEY)

for project in data['data']:
    package_name = project['project_name']
    package_ds = project['description']
    package_more_information = project['more_information']
    package_uris = project['uris']
    if None in package_uris or len(package_uris) == 0: 
        # this most likely means the uris field was not purely a link, meaning there was other text (None case)
        # or there are no csv/geojson/xlsx/shp files in the link (0 length case)
        print(f'Invalid uri field, skipping project: {package_name}')
        continue
    package_org = project['owner_org']

    try:
        print(f'Creating {package_name}')
        package = ckan.action.package_create(name=package_name, notes=package_ds, url = package_more_information, owner_org=package_org)
    except ckanapi.ValidationError as e:
        if e.error_dict.get('__type') == 'Validation Error':
            if 'name' in e.error_dict and e.error_dict['name'] == ['That URL is already in use.']:
                print(f'"{package_name}" package already exists')
                continue # Remove this continue if you want to upload files to an existing project of the same name
                # package = ckan.action.package_show(id=package_name)
                # print(package)
            elif 'owner_org' in e.error_dict:
                print(f"Error: {e.error_dict['owner_org'][0]}")
                sys.exit(1)  # Exit the script if 'owner_org' validation error occurs
            else:
                print(f'Error: {e}')
        else:
            print(f'Error: {e}')
    else:
        print('Package created successfully')

    for url in package_uris:
        filename = url.split("/")[-1]
        response = requests.get(url)

        if response.status_code != 200:
            print(f'Error fetching {url}: {response.content}')
            continue

        file_object = BytesIO(response.content)
        extension = os.path.splitext(filename)[1][1:].upper()
        resource_name = os.path.splitext(filename)[0]
        print(f'Creating "{resource_name}" resource')

        try:
            r = requests.post('http://data.buspark.io/api/3/action/resource_create',
                            data={'package_id': package['name'],
                                    'name': resource_name,
                                    'format': extension,
                                    'url': 'upload',
                                    },
                            headers={'Authorization': MY_API_KEY},
                            files={"upload": file_object})
            r.raise_for_status()
            print(f"printing r: {r}")
            print(f"printing r.content: {r.content}")
            print(f"printing r.json: {r.json()}")
        except requests.HTTPError as e:
            if r.status_code == 409 and 'File upload too large' in r.json()['error'].get('upload', ''):
                print(f'Error: File {resource_name} too large. Skipping...')
                continue
            print(f'HTTP request error while creating resource: {resource_name}, here is the response content: {r.content}')
            print(f'Error: {e}')
        except Exception as e:
            print(f'Error: {e}')

        

