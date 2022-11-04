import requests
import os 

directory = "/path/to/data/directory"

for filename in os.listdir (directory):
    requests.post('http://0.0.0.0:5000/api/action/resource_create',
                  data={"package_id":"my_dataset"},
                  headers={"X-CKAN-API-Key": "21a47217-6d7b-49c5-88f9-72ebd5a4d4bb"},
                  files=[('upload', file(directory + filename))])
    # code from https://docs.ckan.org/en/2.9/maintaining/filestore.html
    # not sure if the part that says 'data={"package_id":"my_dataset"}' needs to be customized 
    # with our own info