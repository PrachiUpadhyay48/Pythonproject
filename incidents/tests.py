from django.test import TestCase

# Create your tests here.
import requests

# Incident Creation
create_incident_url = "http://your-api-endpoint/incidents/create"
incident_data = {
    "title": "Test Incident",
    "description": "This is a test incident",
    "status": "Open"
}
response = requests.post(create_incident_url, json=incident_data)
if response.status_code == 201:
    print("Incident created successfully!")
    incident_id = response.json()["id"]

# Incident Viewing
view_update_incident_url = f"http://your-api-endpoint/incidents/{incident_id}"
response = requests.get(view_incident_url)
if response.status_code == 200:
    incident = response.json()
    print("Incident details:")
    print(incident)

# Incident Editing
update_incident_url = f"http://your-api-endpoint/incidents/{incident_id}"
updated_data = {
    "title": "Updated Incident",
    "description": "This incident has been updated",
    "status": "Closed"
}
response = requests.put(update_incident_url, json=updated_data)
if response.status_code == 200:
    print("Incident updated successfully!")

# Incident Searching
search_incident_url = f"http://your-api-endpoint/incidents/search?incident_id={incident_id}"
response = requests.get(search_incident_url)
if response.status_code == 200:
    incident = response.json()
    print("Search result:")
    print(incident)
