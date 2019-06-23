import geocoder
from darksky import forecast
def get_temp():
    API_KEY = '71f646055b315e115ef69e0b11d1eee4'
    lat, lng = geocoder.ip('me').latlng
    place = forecast(API_KEY, lat, lng)
    f_to_c = lambda f: round((f - 32) * 5.0/9.0)
    temp = f_to_c(place.currently.temperature)
    summary = place.currently.summary
    return (summary, str(temp)+chr(176)+'C')