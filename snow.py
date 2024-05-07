import requests
from requests.auth import HTTPBasicAuth

# Replace these with your ServiceNow instance and credentials
instance_url = 'https://your-instance.service-now.com'
username = 'your_username'
password = 'your_password'

# Endpoint to fetch data, for example, getting incident records
api_endpoint = '/api/now/table/incident'

# Full URL for the request
url = f'{instance_url}{api_endpoint}'

# Make a request using basic authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))

# Check if the request was successful
if response.status_code == 200:
    print('Data retrieved successfully!')
    # Process your data here
    data = response.json()
    print(data)
else:
    print('Failed to retrieve data:', response.status_code)
