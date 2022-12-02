"#!/usr/bin/env python3"

import requests
import os 
from dotenv import load_dotenv
import json
import pandas as pd 
# from urllib.request import urlopen 
import urllib
import urllib.request
import urllib.parse 
import urllib3 
import pprint 
from urllib.parse import urlencode
from bs4 import BeautifulSoup

load_dotenv() 

print("\n\n\n")

API_TOKEN = os.getenv ("API_TOKEN_STG")
SITE_URL = 'http://data.stg.buspark.io'

def read_param_json (param_json): 
   # reads in all of the parameters and does what it needs to do 
   f = open (param_json) 
   params = json.load (f) 
   for key in params.keys():
      param = params[key] 
      # do what needs to be done with the parameters

def create_package (jsonFile): 
   # creating a new package(dataset)
   print ("Creating a new package") 
   print() 
   print ("Previous datasets...")
   prev_datasets = get_datasets() 
   print () 

   http = urllib3.PoolManager(headers = {
   'connection': 'keep-alive',
   'Authorization': API_TOKEN,
   'Content-Type': 'application/json'
   })

   with open(jsonFile) as jsonData:
      DatasetDict = json.load(jsonData)

      request = http.request(
         method='POST', 
         url = f'{SITE_URL}/api/3/action/package_create', 
         body=json.dumps(DatasetDict), 
         headers={'connection': 'keep-alive',
   'Authorization': API_TOKEN,'Content-Type': 'application/json'}
      )

   print ("Updated datasets...")
   new_datasets = get_datasets() 
   print ()

   if len(prev_datasets) < len(new_datasets): 
      print ("Dataset succesfully uploaded")
      return True 
   else: 
      print ("Dataset was not uploaded")
      return False 

def delete_package (package_id): 
   print (f"Deleting package with id: {package_id}") 
   print() 
   print ("Previous datasets...")
   prev_datasets = get_datasets() 
   print () 

   http = urllib3.PoolManager(headers = {
   'connection': 'keep-alive',
   'Authorization': API_TOKEN,
   'Content-Type': 'application/json'
   })

   paramsDict = {"id": package_id}
   request = http.request(
         method='POST', 
         url = f'{SITE_URL}/api/3/action/package_delete', 
         body=json.dumps(paramsDict), 
         headers={'connection': 'keep-alive', 'Authorization': API_TOKEN,'Content-Type': 'application/json'}
   )

   print ("Updated datasets...")
   new_datasets = get_datasets() 
   print ()

   if len(prev_datasets) > len(new_datasets): 
      print ("Dataset succesfully deleted")
      return True 
   else: 
      print ("Dataset was not deleted")
      return False 

def add_resource (id, url, description, filenames_list): 
   params_dict = { 
         "id" : id, 
         "url" : url, 
         "description" : description
   }

   http = urllib3.PoolManager(headers = {
      'connection': 'keep-alive',
      'Authorization': API_TOKEN,
      'Content-Type': 'multipart/form-data'
      })

   # files_to_add = {} 
   # for filename in filenames_list: 
   #    print (filename)
   #    files_to_add [filename] = (filename, open (f"data/{id}/{filename}", "rb"))

   files_to_add = [] 
   for filename in filenames_list: 
      files_to_add.append ('upload', file (f"data/{id}/{filename}"))

   # request = http.request(
   #       method='POST', 
   #       url = f'{SITE_URL}/api/3/action/resource_create', 
   #       body=urllib3.encode_multipart_formdata(files_to_add, boundary=None), 
   #       headers={'connection': 'keep-alive',
   # 'Authorization': API_TOKEN,'Content-Type': 'multipart/form-data'}
   #    )
   request = http.request(
         method='POST', 
         url = f'{SITE_URL}/api/3/action/resource_create', 
         files = files_to_add, 
         headers= {'connection': 'keep-alive', 'Authorization': API_TOKEN,'Content-Type': 'multipart/form-data'}, 
         data = params_dict
   )
   return True 

def upload_all_datasets (full_json): 
   # taking the json with all of the information for each of the projects, uploads the projects to the website 
   f = open (full_json) 
   data = json.load(f) 

   # data_json = json.dumps(data_dict) 

   for project_id in data:
      create_params = { 
         "id": project_id,
         "name": f"project_{project_id}",
         "title": data[project_id]["Project Name"], 
         "private": False, 
         "maintainer": "BU Spark!", 
         "maintainer_email": "spark@bu.edu", 
         "notes": data[project_id]["Project Description"], 
         "url": data[project_id]["Github Link"]
      }

      json_obj = json.dump (create_params, open (f"package{project_id}_params.json", "w"))
      # json_obj = json.loads(temp_str)

      print (type (json_obj))
      # print (type (json.loads(temp_str)))

      package_created = create_package (f"package{project_id}_params.json")
      
      if (package_created): 
         resources_added = add_resource (project_id, data[project_id]["Github Link"], data[project_id]["Project Description"], data[project_id]["File Names"].split(", "))
         if resources_added: 
            print (f"Files successfully uploaded for project id: {project_id}")
         else: 
            print (f"New package created with ID ({project_id}), however, could not add its associated files")
      else: 
         print (f"Files could not be uploaded for project: {data[project_id]['Project Name']} (ID: {project_id}). Package could not be created.")
      # print (f"Trying to upload project {project_id} ({data[project_id]['Project Name']})")
      # response = requests.post (f'{SITE_URL}/api/action/package_create/authorization:{API_TOKEN}', data_json)
      # print (f"\tPackage created? {response}")
      # project_metadata = data[project_id] 
      # add_dataset (project_id, project_metadata)


   # # taking the json with all of the information for each of the projects, uploads the projects to the website 
   # f = open (full_json) 
   # data = json.load(f) 

   # for project_id in data: 
   #    print (f"Trying to upload project {project_id}")
   #    response = requests.post (f'{SITE_URL}/api/action/package_create/authorization:{API_TOKEN}', data_json)
   #    print (f"\tPackage created? {response}")
   #    project_metadata = data[project_id] 
   #    add_dataset (project_id, project_metadata)

def add_dataset (id, metadata): # metadata should be a dict object containing all the metadata for a project 
   all_files = metadata["File Names"]
   file_names = all_files.split (", ")

   response = requests.post(f'{SITE_URL}/api/action/resource_create',
                     data={"Test Dataset 1":"my_dataset"},
                     headers={"X-CKAN-API-Key": API_TOKEN},
                     files=[('upload', open(f"data/1/BPD_personnel_PRR_9_4_2020.xls", encoding = "ISO-8859-1"))])
   print (f"\t {response}")

   # response = requests.post(f'{SITE_URL}/api/action/resource_create',
   #                   data={"package_id":"test1"},
   #                   headers={"X-CKAN-API-Key": API_TOKEN},
   #                   files=[('upload', open(f"data/1/test.txt"))])
   # print (response)

   # for data_file in file_names: 
   #    if not find_dataset (data_file): # only post the data if it is not already on the site 
   #       print (f"Posting {data_file}")
   #       requests.post(f'http://{SITE_URL}/api/action/resource_create',
   #                   data={"package_id":"my_dataset"},
   #                   headers={"X-CKAN-API-Key": API_TOKEN},
   #                   files=[('upload', open(f"data/{id}/{data_file}", encoding = "ISO-8859-1"))])
   #       assert response.code == 200
   #       print (f"Posted {data_file} successfully")
   #    else: 
   #       # remove the dataset already on the site and upload the new one 
   #       print ("Removing datasets not implemented yet")

def get_groups (): 
   # gets the list of all the groups currently on the website 
   response = urllib.request.urlopen (f"{SITE_URL}/api/3/action/group_list")
   response_dict = json.loads(response.read()) 

   if response_dict['success']: 
      print ("Groups Retrieved") 
      print (response_dict['result'])
      return response_dict['result']
   else: 
      print ("An error has occured. Groups were not retrieved.") 
      print (response_dict['error'])
      return None

def get_datasets (): 
   # gets the list of all the datasets that are already on the website 
   response = urllib.request.urlopen (f"{SITE_URL}/api/3/action/package_list")
   response_dict = json.loads(response.read()) 

   if response_dict['success']: 
      print (f"Datasets Retrieved:{response_dict['result']}") 
      return response_dict['result']
   else: 
      print ("An error has occured. Datasets were not retrieved.")
      print (response_dict['error'])
      return None

def get_datasets_and_resources (): 
   # gets the list of all the datasets that are already on the website 
   response = urllib.request.urlopen (f"{SITE_URL}/api/3/action/current_package_list_with_resources")
   response_dict = json.loads(response.read()) 

   if response_dict['success']: 
      print ("Datasets Retrieved.") 
      print (response_dict['result'])
      return response_dict['result']
   else: 
      print ("An error has occured. Datasets were not retrieved.")
      print (response_dict['error'])
      return None

def find_tagged_datasets (tag): 
   # returns a list of all of the datsets on the site that have the given tag 
   response = urllib.request.urlopen (f"{SITE_URL}/api/3/action/package_search?fq=tags:{tag}")
   response_dict = json.loads(response.read()) 

   if response_dict['success']: 
      results = response_dict['result']['results']
      print ("Datasets Retrieved.") 
      print (response_dict['result']['results'])
      return results 
   else: 
      print ("An error has occured. Datasets were not retrieved") 
      print (response_dict['error'])
      return None 

def find_dataset (name_of_dataset): 
   # given the name of a dataset, looks to see if that dataset is already uploaded on the site 
   datasets = get_datasets()
   return name_of_dataset in datasets

# upload_dataset_example() 

# get_datasets_and_resources() 

upload_all_datasets("data/sample.json")

# create_package ("create_package_params/sampletest6.json")
# delete_package ("1")

# get_datasets() 