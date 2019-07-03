import geocoder
from darksky import forecast
import re
from itertools import chain

def get_weather():
    API_KEY = '71f646055b315e115ef69e0b11d1eee4'
    lat, lng = geocoder.ip('me').latlng
    place = forecast(API_KEY, lat, lng)
    f_to_c = lambda f: round((f - 32) * 5.0/9.0)
    temp = f_to_c(place.currently.temperature)
    summary = place.currently.summary
    return (summary, str(temp)+chr(176)+'C')

def validate_name(user_name):
    if not user_name:
        return False
    if len(user_name) < 3 or len(user_name) > 20:
        return False
    return True

def validate_pass(password):
    if password:
        return True
    return False

def validate_email(email):
    if re.match(r'^.+@\w+\.\w{2,3}$', email):
        return True
    return False

def flatten(listOfLists):
    return chain.from_iterable(listOfLists)