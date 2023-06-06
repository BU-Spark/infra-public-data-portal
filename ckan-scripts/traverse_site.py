import os
import ckanapi
from dotenv import load_dotenv
load_dotenv()

MY_API_KEY = os.getenv("API_KEY")


ckan = ckanapi.RemoteCKAN('http://data.buspark.io', apikey=MY_API_KEY)
packages = ckan.action.current_package_list_with_resources()

for package in packages:
    print(f"Package Name: {package['name']}")
    print(f"Package ID: {package['id']}")
    print("Resources:")
    for resource in package['resources']:
        print(f"\tResource Name: {resource['name']}")
        print(f"\tResource ID: {resource['id']}")
