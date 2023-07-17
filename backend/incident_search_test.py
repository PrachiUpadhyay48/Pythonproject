import requests

incident_id = 'ABC123'  # Set the desired incident ID

url = f'http://localhost:8000/incidents/search/?incident_id={incident_id}'
response = requests.get(url)

if response.status_code == 200:
    incident_data = response.json()
    print(f"Incident found: {incident_data}")
else:
    print(f"Incident not found. Error: {response.json()}")
