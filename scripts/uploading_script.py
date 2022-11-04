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

    '''
    This command can be used to overwrite an uploaded file with a new version of the file, 
    post to the resource_update() action and use the upload field: 

    curl -H'Authorization: your-api-key' 'http://yourhost/api/action/resource_update' --form upload=@newfiletoupload --form id=resourceid"
    
    * maybe include a way to check what files have already been uploaded
      (either in a text, json, etc) and then use this command to update 
      that file on the website
    * wrap in os.system() to run the command 
    '''
