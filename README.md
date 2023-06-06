# ckan-scripts

# Project Description
This is an implementation of CKAN for surfacing Spark! and BU data. The aim of the scripts within ckan-scripts is automate the process of creating, modifying, and removing packages and resources from data.buspark.io to make data available to the public. Make sure that you have admin permissions within your organization! 

# Installation Guidelines
There are two other folders, but the scripts are all in ckan-scripts folder. Make sure to have Python installed. The libraries used are os, sys, dotenv, argparse, requests, json, and ckanapi. os, sys, and json should come preinstalled with Python, so you should only have to install dotenv, argparse, requests, and ckanapi.

(I use requests to interface with the official CKAN API and I also use ckanapi library on the side)

# Use
Creating and Uploading a Package:
- Create a json file for the package following the same format as the ones in jsonf
- Create a folder and drop the package's resources (if any) in it
- Navigate to create_dataset.py and change the value of dsCreator to the name of the json file.
- Run the file!

Updating a Package: 
- Give package_update.py permission to be an executable
- This script assumes you know the name of the package and its resources that you want to update, as well as their fields.
- run: package_udpate.py "name_of_the_package_to_be_updated" '{"Update":{"field_name":"new_content"}}' '{"name_of_resource_to_be_updated":{"field_name":"new_content"}}'
- The command above will essentially update the field names that you listed and also the metadata of the resources that you want to update.
- In the second argument of the script, you can include do "Remove": ["field_name"], to remove certain fields. You can also modify the script to handle the deletion of resources (see package_revise in the Official CKAN API Documentation). 

Deleting a Package:
- Give delete.py permission to be an executable
- This script assumes you know the name of the package that you want to delete
- run: delete.py "list_of_packages_to_delete" "0_or_1"
- 0 removes the dataset from the frontend, whereas 1 removes the dataset entirely from the database. 

Notes:
There are additional scripts that provide helpful information. org_id.py returns the organization ID which is requried in some api calls. traverse_site.py returns all the packages and their resources within your organization. Feel free to make your own individual functions that perform simple tasks well and incorporate them into the larger scripts eg. a function that deletes a resource. 
