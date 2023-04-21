import ckanapi
import os
from dotenv import load_dotenv
load_dotenv()

MY_API_KEY = os.getenv("API_KEY")
ckan = ckanapi.RemoteCKAN('http://data.buspark.io', apikey=MY_API_KEY)
org_name = 'buspark'
org_data = ckan.action.organization_show(id=org_name)
org_id = org_data['id']
print('Organization ID:', org_id)

