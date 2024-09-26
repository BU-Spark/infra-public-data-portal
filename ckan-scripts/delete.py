#!/usr/bin/env python
import argparse
import json
import os
import requests
from dotenv import load_dotenv
import ckanapi
load_dotenv()
import time

"""
Description of the file/module.

Args:
    arg1 (list): list of names of the package to be deleted 
    arg2 (int): 0 will remove the package from the frontend. 1 will permanantly remove the package from the CKAN database.
    arg2 should be a flag default should be remove and purge should be extra effort
Example:
    python3 delete.py "risk_evaluator" "0"
"""
def isArray(inp):
    try:
        array = json.loads(inp)
        return array
    except ValueError:
        print('input is not a valid JSON array')
MY_API_KEY = os.getenv("API_KEY")
ORGANIZATION_ID = os.getenv("ORGANIZATION_ID")
HEADERS = {
    'Authorization': MY_API_KEY
}

parser = argparse.ArgumentParser()
parser.add_argument(
    "package_name",
    help="list of packages you want to delete",
    type=isArray
)

parser.add_argument(
    "method",
    help="0: remove the package from frontend (still in CKAN Database)\n 1: remove the package from the CKAN database permanantly",
    type=int
)

args = parser.parse_args()
# Grabbing user inputs
package_name = args.package_name
update = args.method

#set up dataset_purge and package_delete methods both use a data_dict of string ID

def get_package_data(names):
    """Return the id of a package provided through the name argument.
    
    Args:
        name: name of the package
    """
    to_delete = names
    package_ids = {}
    ids = []
    ckan = ckanapi.RemoteCKAN('http://data.buspark.io', apikey=MY_API_KEY)
    packages = ckan.action.current_package_list_with_resources()
    try:
        for package in packages:
            package_ids[package['name']]= package['id']
        for name in to_delete:
            if name not in package_ids.keys():
                raise KeyError(f"Package {name} does not exist ")
            else:
                ids.append(package_ids[name])
        return ids
    except KeyError as e:
        raise e
    
def delete_package(idList, method):
    url = ''
    if method == 0:
        url = 'http://data.buspark.io/api/3/action/package_delete'
    else:
        url = 'http://data.buspark.io/api/3/action/dataset_purge'
    data_dict = {}
    print(idList)
    #if len(idList)>1:
      #  data_dict = {
       #     "id": f"{id}",
        #    "organization_id": f"{ORGANIZATION_ID}"
       # }
       # url = 'http://data.buspark.io/api/3/action/bulk_update_delete'
    for ID in idList:
        data_dict = {
            "id": f"{ID}"
        }
        response = requests.post(url, data=data_dict, headers=HEADERS)
        response_dict = response.json()
        json_pretty = json.dumps(response_dict, indent=2)
        print(json_pretty)
        print(url)
        time.sleep(2)
        
PID = get_package_data(package_name)
delete_package(PID, 1)


        
