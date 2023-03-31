import ckanapi
import os
from dotenv import load_dotenv

load_dotenv()
my_API_KEY = os.getenv("API_KEY")

APIKEY = my_API_KEY
#this code does not iterate over json files right now 
#read JSON file 

ckan = ckanapi.RemoteCKAN('http://data.buspark.io', apikey=APIKEY)

packages = ckan.action.current_package_list_with_resources()

# print the package list and resources
for package in packages:
    print(f"Package Name: {package['name']}")
    print(f"Package ID: {package['id']}")
    print("Resources:")
    for resource in package['resources']:
        print(f"\tResource Name: {resource['name']}")
        print(f"\tResource ID: {resource['id']}")