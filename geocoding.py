import googlemaps
from django.conf import settings


def get_city_and_country(pin_code):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    geocode_result = gmaps.geocode(pin_code)
    city = None
    country = None

    if geocode_result:
        address_components = geocode_result[0]['address_components']
        for component in address_components:
            if 'locality' in component['types']:
                city = component['long_name']
            elif 'country' in component['types']:
                country = component['long_name']

    return city, country
