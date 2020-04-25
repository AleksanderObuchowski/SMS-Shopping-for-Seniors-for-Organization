import requests
import json

geocoder_url = 'https://us1.locationiq.com/v1/search.php'
geocoder_api = '81a3bf223e5959'
geocoder_data = {
    'key': geocoder_api,
    'q': '',
    'format': 'json'
}

def get_location(message,search = True):
    if search:
        pass
    else:
        geocoder_data['q'] = message
        location = requests.get(geocoder_url, params=geocoder_data)
        if 'error' not in location.json():
            lat = float(location.json()[0]['lat'])
            lon = float(location.json()[0]['lon'])
            return message, lat, lon
        else:
            return 'unk', 'unk', 'unk'