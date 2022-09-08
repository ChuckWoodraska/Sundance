import pymysql.cursors
from geopy.geocoders import Nominatim
import urllib
import json
import time
import configparser
import os

geolocator = Nominatim()
location = geolocator.reverse("32.90, -79.89")
baseurl = "https://query.yahooapis.com/v1/public/yql?"
yql_query = f"select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='{location.raw['address']['city']}, {location.raw['address']['state']}')"

yql_url = baseurl + urllib.parse.urlencode({'q': yql_query}) + "&format=json"
result = urllib.request.urlopen(yql_url).read()
data = json.loads(result.decode('utf-8'))
short_data = data['query']['results']['channel']
sunrise = time.strptime(data['query']['results']['channel']['astronomy']['sunrise'], "%I:%M %p")
weather_data = {
    'temp': short_data['item']['condition']['temp'],
    'code': short_data['item']['condition']['code'],
    'today_code': short_data['item']['forecast'][0]['code'],
    'high': short_data['item']['forecast'][0]['high'],
    'low': short_data['item']['forecast'][0]['low'],
    'wind_chill': short_data['wind']['chill'],
    'wind_direction': short_data['wind']['direction'],
    'wind_speed': short_data['wind']['speed'],
    'humidity': short_data['atmosphere']['humidity'],
    'pressure': short_data['atmosphere']['pressure'],
    'rising': short_data['atmosphere']['rising'],
    'visibility': short_data['atmosphere']['visibility'],
    'forecast_low1': short_data['item']['forecast'][1]['low'],
    'forecast_high1': short_data['item']['forecast'][1]['high'],
    'forecast_code1': short_data['item']['forecast'][1]['code'],
    'forecast_low2': short_data['item']['forecast'][2]['low'],
    'forecast_high2': short_data['item']['forecast'][2]['high'],
    'forecast_code2': short_data['item']['forecast'][2]['code'],
    'forecast_low3': short_data['item']['forecast'][3]['low'],
    'forecast_high3': short_data['item']['forecast'][3]['high'],
    'forecast_code3': short_data['item']['forecast'][3]['code'],
    'forecast_low4': short_data['item']['forecast'][4]['low'],
    'forecast_high4': short_data['item']['forecast'][4]['high'],
    'forecast_code4': short_data['item']['forecast'][4]['code'],
    'city': short_data['location']['city'],
    'country': short_data['location']['country'],
    'region': short_data['location']['region'],
    'sunrise': int(time.strftime("%H%M", sunrise)),
}

sunset = time.strptime(data['query']['results']['channel']['astronomy']['sunset'], "%I:%M %p")
weather_data['sunset'] = int(time.strftime("%H%M", sunset))

config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))
connection = pymysql.connect(config['DATABASE']['HOST'], config['DATABASE']['DBUSER'], config['DATABASE']['DBPASS'],
                             config['DATABASE']['DBNAME'], cursorclass=pymysql.cursors.DictCursor)
try:
    with connection.cursor() as cursor:
        sql = "INSERT INTO weather (temp, code, today_code, high, low, wind_chill, wind_direction, wind_speed, humidity," \
              "pressure, rising, visibility, forecast_low1, forecast_high1, forecast_code1, forecast_low2, forecast_high2," \
              "forecast_code2, forecast_low3, forecast_high3, forecast_code3, forecast_low4, forecast_high4, forecast_code4," \
              "sunrise, sunset, city, country, region) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
              "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        sql_params = [weather_data['temp'], weather_data['code'], weather_data['today_code'],
                      weather_data['high'], weather_data['low'], weather_data['wind_chill'],
                      weather_data['wind_direction'],
                      weather_data['wind_speed'], weather_data['humidity'], weather_data['pressure'],
                      weather_data['rising'],
                      weather_data['visibility'],
                      weather_data['forecast_low1'], weather_data['forecast_high1'], weather_data['forecast_code1'],
                      weather_data['forecast_low2'], weather_data['forecast_high2'], weather_data['forecast_code2'],
                      weather_data['forecast_low3'], weather_data['forecast_high3'], weather_data['forecast_code3'],
                      weather_data['forecast_low4'], weather_data['forecast_high4'], weather_data['forecast_code4'],
                      weather_data['sunrise'], weather_data['sunset'], weather_data['city'], weather_data['country'],
                      weather_data['region']]
        cursor.execute(sql, sql_params)
        connection.commit()
finally:
    connection.close()
