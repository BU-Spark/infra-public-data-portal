import requests
import os 
import json
import pandas as pd 
# from urllib.request import urlopen 
import urllib.request
import urllib.parse 

API_TOKEN = os.getenv ("API_TOKEN")
SITE_URL = 'http://data.stg.buspark.io'

# directory = "/path/to/data/directory"

# for filename in os.listdir (directory):
#     requests.post('http://0.0.0.0:5000/api/action/resource_create',
#                   data={"package_id":"my_dataset"},
#                   headers={"X-CKAN-API-Key": "21a47217-6d7b-49c5-88f9-72ebd5a4d4bb"},
#                   files=[('upload', file(directory + filename))])
#     # code from https://docs.ckan.org/en/2.9/maintaining/filestore.html
#     # not sure if the part that says 'data={"package_id":"my_dataset"}' needs to be customized 
#     # with our own info

def read_param_json (param_json): 
   # reads in all of the parameters and does what it needs to do 
   f = open (param_json) 
   params = json.load (f) 
   for key in params.keys():
      param = params[key] 
      # do what needs to be done with the parameters

def upload_dataset_example (): # doesn't work atm
   # code block from the CKAN website 

   # Put the details of the dataset we're going to create into a dict.
   dataset_dict = {
      'name': 'Test 1',
      'notes': 'A long description of my dataset',
      'file_path': "data/test_set1.xls"
   }

   # Use the json module to dump the dictionary to a string for posting.
   data_string = urllib.parse.quote(json.dumps(dataset_dict))
   data = urllib.parse.urlencode(dataset_dict).encode("utf-8")

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
   for project_id in data: 
      project_metadata = data[project_id] 
      add_dataset (project_id, project_metadata)

def add_dataset (id, metadata): # metadata should be a dict object containing all the metadata for a project 
   # f = open (metadata_json) 
   # data = json.load (metadata_json) 
   all_files = metadata["File Names"]
   file_names = all_files.split (", ")
   for data_file in file_names: 
      if not find_dataset (data_file): # only post the data if it is not already on the site 
         print (f"Posting {data_file}")
         requests.post(f'http://{SITE_URL}/api/action/resource_create',
                     data={"package_id":"my_dataset"},
                     headers={"X-CKAN-API-Key": API_TOKEN},
                     files=[('upload', open(f"data/{id}/{data_file}", encoding = "ISO-8859-1"))])
         print (f"Posted {data_file} successfully")
      else: 
         # remove the dataset already on the site and upload the new one 
         print ("Removing datasets not implemented yet")

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
upload_all_datasets("data/sample.json")
