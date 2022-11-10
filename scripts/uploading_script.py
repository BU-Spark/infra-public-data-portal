import requests
import os 
import json
import pandas as pd 

file_extensions = [".csv", ".xlsx", ".zip"]
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
   #  requests.post('http://0.0.0.0:5000/api/action/resource_create',
   #                data={"package_id":"my_dataset"},
   #                headers={"X-CKAN-API-Key": "21a47217-6d7b-49c5-88f9-72ebd5a4d4bb"},
   #                files=[('upload', file("../" + data["Datasets"]))])
    print (data) 


add_dataset ("../jsons/row1.json")
c = pd.read_csv ("https://github.com/BU-Spark/summer2021internship/blob/master/Police%20Arrest%20Analysis/cumulativeNIBRS.csv")
print (c)
'''
0.0.0.0 -> data.buspark.io, keep port 
get api key by making an account (go to http://data.buspark.io) and 

figure out the best way to show that data
figure out metadata format (json file, what's the name of the project, what other data do we want to show, the year it was created" 

let this python script take a parameter which would be the metadata 
data: csv files 
metadata: info about the csv files 
dataset: not a single csv, a whole blob of files 


the way langdon wants us to write the script 
 * create a json file with name value pairs with the metadata 
 * first pass is 
 * a series of assignments 
 * go through json file and substitute it to the api with placeholders 
 * json decoder in python 
 * have  constatn which is the api call 
    * use <api_key> so you can insert that info into the <> 
 * store all the metadata in ckan 
 * separate into functions 
    * create data_set 
    * push data_set 
    * takes parameters 
 * in first pass maybe just try with single files 
 * make a json with all the arguments that would be passed into the script so instead of writing "py uploading_script.py arg1 arg2 arg3", make a json with all the args 
'''


'''
This command can be used to overwrite an uploaded file with a new version of the file, 
post to the resource_update() action and use the upload field: 

curl -H'Authorization: your-api-key' 'http://yourhost/api/action/resource_update' --form upload=@newfiletoupload --form id=resourceid"

* maybe include a way to check what files have already been uploaded
(either in a text, json, etc) and then use this command to update 
that file on the website
* wrap in os.system() to run the command 
'''
