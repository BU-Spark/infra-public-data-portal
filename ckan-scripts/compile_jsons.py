"""
The purpose of this script is to take in the spreadsheet with responses to the gform, 
and create a JSON file with all the required metadata fields to be passed to create_datasets.py

Currently only works for data stored in a GitHub repo or Google Drive

Note: manually reads in csv using pandas
"""

import pandas as pd
import json
import datetime
import requests
import re
from urllib.parse import urlparse
from datetime import datetime

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    
def link_transformation(x):
    if is_valid_url(x) and pd.notna(x):
        if x.startswith('https://github.com/'):
            return get_raw_urls(x)  # Assuming this function processes GitHub URLs
        elif x.startswith('https://drive.google.com/'):
            return [x]  # Return the Google Drive link in a list
    return [None]

def get_raw_urls(repo_url):
    # Extract the username, repository name, and path from the URL
    parts = repo_url.split("/")
    user = parts[3]
    repo = parts[4]
    path = "/".join(parts[7:])  # Get the path inside the repository

    api_url = f"https://api.github.com/repos/{user}/{repo}/contents/{path}"

    response = requests.get(api_url)
    response.raise_for_status()
    contents = response.json()

    # Filter for specific file extensions and construct raw URLs
    raw_urls = []
    for item in contents:
        if item['type'] == 'file' and any(item['name'].endswith(ext) for ext in ['.csv', '.xlsx', '.shp', '.geojson']):
            raw_url = item['download_url']
            raw_urls.append(raw_url)
            
    return raw_urls


# read in csv manually  for now
df = pd.read_csv('FINALDATAATSPARKTEST.csv')

# Rename columns, based on form in August 2023
df.rename({'What is the project name?': 'project_name',
            'What is this project about? What is the goal of this project?': 'description',
            "What is the link to your project's GitHub repository? Please provide the link below. ": 'more_information',
            'What data sets did you use in your project? Please provide the link. ': 'uris'}, axis=1, inplace=True)

cols_to_keep = ['project_name', 'description', 'more_information', 'uris']
drop = [col for col in df.columns if col not in cols_to_keep ]
df.drop(drop, axis=1, inplace=True)

# Create owner_org field, set all to buspark
df['owner_org'] = 'buspark'

# Rename project_names, need to be alphanumeric, underscores, etc
df['project_name'] = df['project_name'].str.replace(" ", "_")
regex = re.compile('[^a-zA-Z0-9_]')
df['project_name'] = df['project_name'].apply(lambda x: regex.sub('', x).lower())

# Get raw github urls
# df['uris'] = df['uris'].apply(lambda x: get_raw_urls(x) if is_valid_url(x) and pd.notna(x) else [None])
df['uris'] = df['uris'].apply(link_transformation)


# save as JSON file
data_dict = df.to_dict('records')
json_data = {"data": data_dict}

# Get today's date in YYYY-MM-DD format
today = datetime.now().strftime('%Y-%m-%d-%H:%M')

# Define filename with today's date
filename = f'spark_datasets_{today}.json'

# Write to file with indentation
with open(filename, 'w') as f:
    json.dump(json_data, f, indent=4)
