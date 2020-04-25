import requests
import json
from polyglot.text import Text
from twilio.rest import Client


from zakupy_dla_seniora.config import twilio_sid, twilio_auth_token, twilio_phone
from zakupy_dla_seniora.messages.models import Messages


client = Client(twilio_sid, twilio_auth_token)

geocoder_url = 'https://us1.locationiq.com/v1/search.php'
geocoder_api = '81a3bf223e5959'
geocoder_data = {
    'key': geocoder_api,
    'q': '',
    'format': 'json'
}

def get_location(message,search = True):
    if search:
        text = Text(message)
        for ent in text.entities:
            if ent.tag in ['I-LOC', 'I-ORG']:
                geocoder_data['q'] = ent
                location = requests.get(geocoder_url, params=geocoder_data)
                if 'error' not in location.json():
                    lat = float(location.json()[0]['lat'])
                    lon = float(location.json()[0]['lon'])
                    return ent, lat, lon
                else:
                    return 'unk', 'unk', 'unk'

        return None, None, None
    else:
        geocoder_data['q'] = message
        location = requests.get(geocoder_url, params=geocoder_data)
        if 'error' not in location.json():
            lat = float(location.json()[0]['lat'])
            lon = float(location.json()[0]['lon'])
            return message, lat, lon
        else:
            return None, None, None
def respond(response,phone_number):
    client.messages.create(
        to=phone_number,
        from_=twilio_phone,
        body=response,
    )

def conversation(last_message, content,phone_number):
    try:

        if not last_message or last_message.status == 'ended':

            ent, lat, lon = get_location(content)
            if None in [ent, lat, lon]:
                message = Messages(content=content, location=ent, longitude=lon, latitude=lat,
                                   contact_number=phone_number,
                                   status='waiting for location')
                message.save()
                response = "We didn't get your location, can you type it again?"
                return {'success': True, 'response': response}, 200
            else:
                message = Messages(content=content, location=ent, longitude=lon, latitude=lat,
                                   contact_number=phone_number,
                                   status='received')
                message.save()
                response = 'Thanks, we will let you know once someone volunteers to do your shopping'
        elif last_message.status == 'waiting for location':
            ent, lat, lon = get_location(content, search=False)
            if None in [ent, lat, lon]:
                response = "We still didn't get your location, can you type it again?"

                return {'success': True, 'response': response}, 200
            else:
                last_message.status = 'received'
                last_message.longitude = lon
                last_message.latitude = lat
                last_message.location = ent
                last_message.save()

                response = 'Thanks, we will let you know once someone volunteers to do your shopping'
                return {'success': True, 'response': response}, 200

        elif last_message.status == 'taken':
            last_message.status = 'waiting for end'
            last_message.location = content
            last_message.save()
            response = 'Got it! Your volunteer will be there shortly, stay tuned!'
            return {'success': True, 'response': response}, 200
        elif last_message.status == 'waiting for feedback':
            if content.lowercase() in ['ok', 'okey', 'yes', 'thanks']:
                last_message.status = 'ended'
                last_message.save()
                response = 'Thanks! If you need us again, please write new message same as before!'
                return {'success': True, 'response': response}, 200
            else:
                last_message.status = 'error'
                last_message.error = content
                last_message.save()
                response = 'Thank you for your feedback, someone will contact you shortly'
                return {'success': True, 'response': response}, 200

        else:
            last_message.status = 'error'
            last_message.error = 'unknown state'
            last_message.save()
            response = 'Something went wrong, someone will contact you shortly'
            return {'success': False, 'response': response}, 200

    except Exception as e:
        if not 'last_message' in locals() or last_message.status == 'ended':
            content = content if 'content' in locals() else None
            phone_number = phone_number if 'phone_number' in locals() else None

            message = Messages(content=content, contact_number=phone_number, status='error')
            message.save()
            response = 'Something went wrong, someone will contact you shortly'
            return {'success': False, 'response': 'error'}, 200

        else:
            last_message.status = 'error'
            last_message.error = e
            last_message.save()
            response = 'Something went wrong, someone will contact you shortly'
            return {'success': False, 'response': 'error'}, 200
