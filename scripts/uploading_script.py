import requests
import os 
import json
import pandas as pd 

file_extensions = [".csv", ".xlsx", ".zip"]
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJ0QlNLV29XYTN1R2NDeEZTU1EtREh5ekNfaUhhRWNTQzFRUmtQRTVnaFgwIiwiaWF0IjoxNjY4MjYyNTM1fQ.SjGtjmAexPLECZmnV8OuCUWuosgiHNwzpq_SSjNqK0E"
# directory = "/path/to/data/directory"

# for filename in os.listdir (directory):
#     requests.post('http://0.0.0.0:5000/api/action/resource_create',
#                   data={"package_id":"my_dataset"},
#                   headers={"X-CKAN-API-Key": "21a47217-6d7b-49c5-88f9-72ebd5a4d4bb"},
#                   files=[('upload', file(directory + filename))])
#     # code from https://docs.ckan.org/en/2.9/maintaining/filestore.html
#     # not sure if the part that says 'data={"package_id":"my_dataset"}' needs to be customized 
#     # with our own info

def add_dataset (metadata_json): 
    f = open (metadata_json) 
    data = json.load (f)
    requests.post('http://{API-TOKEN}:5000/api/action/resource_create',
                  data={"package_id":"my_dataset"},
                  headers={"X-CKAN-API-Key": API_TOKEN},
                  files=[('upload', file("data/" + data["Datasets"]))])
    print (data) 


add_dataset ("jsons/row1.json")
c = pd.read_csv ("https://github.com/BU-Spark/summer2021internship/blob/master/Police%20Arrest%20Analysis/cumulativeNIBRS.csv", on_bad_lines='skip')
print (c)