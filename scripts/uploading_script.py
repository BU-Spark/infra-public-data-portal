import requests
import os 
import json
import pandas as pd 
# from urllib.request import urlopen 
import urllib.request

file_extensions = [".csv", ".xlsx", ".zip"]
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJ0QlNLV29XYTN1R2NDeEZTU1EtREh5ekNfaUhhRWNTQzFRUmtQRTVnaFgwIiwiaWF0IjoxNjY4MjYyNTM1fQ.SjGtjmAexPLECZmnV8OuCUWuosgiHNwzpq_SSjNqK0E"
SITE_URL = 'http://data.buspark.io'

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


def add_dataset (metadata_json): 
   '''
   metadata includes: 
   - project name 
   - association/group it is part of 
   - project description 
   - github link 
   - link to data sets 
   - file names 
   - notes about the data set 
   '''
   f = open (metadata_json) 
   data = json.load (f) 
   all_files = data["File Names"]
   file_names = all_files.split (", ")
   for data_file in file_names: 
      if not find_dataset (data_file): # only post the data if it is not already on the site 
         requests.post(f'http://{SITE_URL}/api/action/resource_create',
                     data={"package_id":"my_dataset"},
                     headers={"X-CKAN-API-Key": API_TOKEN},
                     files=[('upload', file(f"data/{data_file}"))])
      else: 
         # remove the dataset already on the site and upload the new one 
         pass 

   print (data) 

def get_groups (): 
   # gets the list of all the groups currently on the website 
   response = urllib.request.urlopen (SITE_URL + "/api/3/action/group_list")
   response_dict = json.loads(response.read()) 

   if response_dict['success']: 
      # print (response_dict['result'])
      return response_dict['result']
   else: 
      print (response_dict['error'])
      return None

def get_datasets (): 
   # gets the list of all the datasets that are already on the website 
   response = urllib.request.urlopen (SITE_URL + "/api/3/action/package_list")
   response_dict = json.loads(response.read()) 

   if response_dict['success']: 
      # print (response_dict['result'])
      return response_dict['result']
   else: 
      print (response_dict['error'])
      return None

def find_tagged_datasets (tag): 
   # returns a list of all of the datsets on the site that have the given tag 
   response = urllib.request.urlopen (SITE_URL + f"/api/3/action/package_search?fq=tags:{tag}")
   response_dict = json.loads(response.read()) 

   if response_dict['success']: 
      results = response_dict['result']['results']
      return results 
   else: 
      print (response_dict['error'])
      return None 

def find_dataset (name_of_dataset): 
   # given the name of a dataset, looks to see if that dataset is already uploaded on the site 
   datasets = get_datasets()
   return name_of_dataset in datasets