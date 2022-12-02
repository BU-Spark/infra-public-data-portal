"#!/usr/bin/env python3"

import requests
import os 
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

print("\n\n\n")

# API_TOKEN = os.getenv ("API_TOKEN_STG")
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0TGdsNUJiTVpQdW41U1p5NFlZbU9hT09WQU5MV1hJTmpIQk5vVThEZnNzIiwiaWF0IjoxNjY5NjQ5NzcyfQ.cE3hjaVun5E32ZYYFQi3PTIbQqba8YcKVUmYCmieUEM"
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

   prev_datasets = get_datasets() 

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

      # json.loads(request.data.decode('utf-8'))['json']

      # soup = BeautifulSoup(request.data, features="lxml")


      # response = urllib.request.urlopen(request, data=None)
      # assert response.code == 200

      # response_dict = json.loads(response.read())
      # assert response_dict['success'] is True

   new_datasets = get_datasets() 

   if len(prev_datasets) < len(new_datasets): 
      print ("Dataset succesfully uploaded")
   else: 
      print ("Dataset was not uploaded")

def upload_dataset_example (): # doesn't work atm
   # code block from the CKAN website 

   # Put the details of the dataset we're going to create into a dict.
   # dataset_dict = {
   #    'name': 'Test 1',
   #    'notes': 'A long description of my dataset',
   #    'file_path': "data/1/BPD_personnel_PRR_9_4_2020.xls"#test_set1.xls"
   # }
   dataset_dict = { 
      "id":"Test", 
      "name": "Test Dataset 1",
      "private": False, 
      "maintainer": "BU Spark!", 
      "maintainer_email": "spark@bu.edu", 
      "notes": "Here is a sample dataset.", 
      "url": "https://github.com/BU-Spark/CS506-Fall2020-Projects/tree/master/police_conduct_data/final_deliverable" 
   }

   # Use the json module to dump the dictionary to a string for posting.
   data_string = urllib.parse.quote(json.dumps(dataset_dict))
   # data = urllib.parse.urlencode(dataset_dict).encode("UTF-8")

   # We'll use the package_create function to create a new dataset.
   request = urllib.request.Request(f'{SITE_URL}/api/action/package_create')

   # Creating a dataset requires an authorization header.
   # Replace *** with your API key, from your user account on the CKAN site
   # that you're creating the dataset on.
   request.add_header('Authorization', API_TOKEN)

   # Make the HTTP request.
   response = urllib.request.urlopen(request, data=None)
   assert response.code == 200

   # Use the json module to load CKAN's response into a dictionary.
   response_dict = json.loads(response.read())
   assert response_dict['success'] is True

   # package_create returns the created package as its result.
   created_package = response_dict['result']
   pprint.pprint(created_package)

def upload_all_datasets (full_json): 
   # taking the json with all of the information for each of the projects, uploads the projects to the website 
   f = open (full_json) 
   data = json.load(f) 

   data_dict = { 
      "name": "Test Dataset 1",
      "private": False, 
      "maintainer": "BU Spark!", 
      "maintainer_email": "spark@bu.edu", 
      "notes": "Here is a sample dataset.", 
      "url": "https://github.com/BU-Spark/CS506-Fall2020-Projects/tree/master/police_conduct_data/final_deliverable" 
   }

   data_json = json.dumps(data_dict) 

   for project_id in data: 
      print (f"Trying to upload project {project_id} ({data[project_id]['Project Name']})")
      response = requests.post (f'{SITE_URL}/api/action/package_create/authorization:{API_TOKEN}', data_json)
      print (f"\tPackage created? {response}")
      project_metadata = data[project_id] 
      add_dataset (project_id, project_metadata)


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

# upload_all_datasets("data/sample.json")

create_package ("sample2.json")

# get_datasets() 