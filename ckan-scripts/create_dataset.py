#!/usr/bin/env python
"""
The purpose of this script is to take in the json file produced by compile_json.py and upload all of the projects to our 
Data@Spark website.

Again, only works for data stored in GitHub repos and Google Drive folders
"""
import ckanapi
import requests
import sys
import os
import json
from io import BytesIO

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import pickle

"""
SETTING UP GOOGLE DRIVE API

First time generating token.pkl, must sign in using BU email, also beforehand must create credentials.json
"""

# OAuth2.0 scope for read-only access to file metadata and file content
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Your credentials.json file (downloaded from the Developer Console)
CREDENTIALS_FILE = 'andyyangcredentials.json'

# Path to token file
TOKEN_FILE = 'token.pkl'

# Check if token file exists
if os.path.exists(TOKEN_FILE):
    print("found token")
    with open(TOKEN_FILE, 'rb') as token_file:
        creds = pickle.load(token_file)
else:
    # OAuth2.0 flow
    print("no token found")
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    flow.redirect_uri = 'http://localhost:8080/'
    creds = flow.run_local_server(port=8080)

    # Save the credentials for the next run
    with open(TOKEN_FILE, 'wb') as token_file:
        pickle.dump(creds, token_file)

print("building drive_service")
drive_service = build('drive', 'v3', credentials=creds)

def get_folder_id_from_url(url):
    return url.split('/')[-1].split('?')[0]

"""
CREATING FUNCTIONS TO HANDLE DIFFERENT URIS TO UPLOAD: GITHUB AND DRIVE FOLDERS
"""

# Function to download files from Google Drive folder
def download_from_google_drive(folder_url):
    # Find the folder using the folder id
    folder_id = get_folder_id_from_url(folder_url)
    query = f"'{folder_id}' in parents"
    results = drive_service.files().list(
        q=query,
        pageSize=10,
        fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get('files', [])
    
    # Append the csvs to a list
    # https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.http.MediaIoBaseDownload-class.html
    files = []
    for item in items:
        if item['mimeType'] == 'text/csv':
            print(f"Downloading file {item['name']} with ID {item['id']}") 
            file_id = item['id']
            request = drive_service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            fh.seek(0)
            content = fh.read()
            files.append((item['name'], content))
    return files


# Function to download files from raw.githubusercontent link, just a GET req
def download_from_github(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f'Error fetching {url}: {response.content}')
        return []
    return [(url.split("/")[-1], response.content)]

# Function to upload to CKAN
def upload_to_ckan(filename, content, package):
    file_object = BytesIO(content)
    extension = os.path.splitext(filename)[1][1:].upper()
    resource_name = os.path.splitext(filename)[0]
    print(f'Creating "{resource_name}" resource')

    try:
        r = requests.post('http://data.buspark.io/api/3/action/resource_create',
                        data={'package_id': package['name'],
                                'name': resource_name,
                                'format': extension,
                                'url': 'upload',
                                },
                        headers={'Authorization': MY_API_KEY},
                        files={"upload": file_object})
        r.raise_for_status()
    except requests.HTTPError as e:
        if r.status_code == 409 and 'File upload too large' in r.json()['error'].get('upload', ''):
            print(f'Error: File {resource_name} too large. Skipping...')
        else:
            print(f'HTTP request error while creating resource: {resource_name}, here is the response content: {r.content}')
            print(f'Error: {e}')
    except Exception as e:
        print(f'Error: {e}')



"""
CREATE THE NEW DATASET AND PROCESS THE DATA
"""

# env variable in the future
MY_API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJoOEdpRWVKLUhtWk9wQmlRbFJGNE1wTHNOR1hoWEowX1ZaRVV6YU1QV0xVIiwiaWF0IjoxNjkyMjQ1ODc4fQ.4SUKvCt8ctqQ2-NF23FlKT5bsLxliq_EwE2dfix3BCI"

all_projects = 'spark_datasets_2023-08-17-00:07.json'

with open(all_projects) as f:
    data = json.load(f)

ckan = ckanapi.RemoteCKAN('http://data.buspark.io', apikey=MY_API_KEY)

for project in data['data']:
    package_name = project['project_name']
    package_ds = project['description']
    package_more_information = project['more_information']
    package_uris = project['uris']
    if None in package_uris or len(package_uris) == 0: 
        # this most likely means the form response was not purely a link, meaning there was other text (None case)
        # or there are no csv/geojson/xlsx/shp files in the github repo (0 length case)
        print(f'Invalid uri field, skipping project: {package_name}')
        continue
    package_org = project['owner_org']

    try:
        print(f'Creating {package_name}')
        package = ckan.action.package_create(name=package_name, notes=package_ds, url = package_more_information, owner_org=package_org)
    except ckanapi.ValidationError as e:
        if e.error_dict.get('__type') == 'Validation Error':
            if 'name' in e.error_dict and e.error_dict['name'] == ['That URL is already in use.']:
                print(f'"{package_name}" package already exists')
                continue
                # package = ckan.action.package_show(id=package_name)
                # print(package)
            elif 'owner_org' in e.error_dict:
                print(f"Error: {e.error_dict['owner_org'][0]}")
                sys.exit(1)  # Exit the script if 'owner_org' validation error occurs
            else:
                print(f'Error: {e}')
        else:
            print(f'Error: {e}')
    else:
        print('Package created successfully')

    for url in package_uris:
        # Determine whether it's GitHub or Google Drive
        if url.startswith('https://raw.githubusercontent.com'):
            files = download_from_github(url)
        elif url.startswith('https://drive.google.com/'):
            files = download_from_google_drive(url)
        else:
            print(f'Unknown link: {url}')
            continue

        # Upload the files to CKAN
        for filename, content in files:
            upload_to_ckan(filename, content, package)


        

