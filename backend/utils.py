import requests
from django import forms
from django.contrib.auth.models import User


def get_city_and_country(pin_code):
    url = f"https://nominatim.openstreetmap.org/search?postalcode={pin_code}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            city = data[0].get("address", {}).get("city")
            country = data[0].get("address", {}).get("country")
            return city, country
    return None, None


