import requests
from getpass import getpass
import time
import random
import math


def authenticate(username, password):
    url = 'http://127.0.0.1/api/token-auth/'
    data = {
        'username': username,
        'password': password
    }
    r = requests.post(url, data=data)
    return r.json()


def get_float(message):
    while True:
        try:
            response = float(input(message))
        except ValueError:
            print('The input you provided is not a valid floating number. Please try again.')
            continue
        else:
            break
    return response


def compute_distance(coord_1, coord_2):
    delta_1 = coord_2[0] - coord_1[0]
    delta_2 = coord_2[1] - coord_1[1]

    latitude_sinus = math.sin(delta_1 / 2.0)
    longitude_sinus = math.sin(delta_2 / 2.0)

    tmp = latitude_sinus ** 2 + math.cos(coord_1[0]) * math.cos(coord_2[0]) * longitude_sinus ** 2
    tmp = 2 * math.asin(math.sqrt(tmp))
    return tmp * 6371000


def generate_out_of_bounds(name):
    return '{} has gone out of the restricted area.'.format(name)


class Kid(object):
    def __init__(self, token, kid_id):
        self.token = token
        self.id = kid_id
        self.location_url = 'http://127.0.0.1/api/location/'
        self.notification_url = 'http://127.0.0.1/api/notification/'
        self.weather_link = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=meters'
        self.kid_url = 'http://127.0.0.1/api/kid/{}'.format(self.id)
        self.check_kid_resource()

    def check_kid_resource(self):
        headers = {'Authorization': 'Token {}'.format(self.token)}
        response = requests.get(self.kid_url, headers=headers).json()
        if 'detail' in response:
            print(response['detail'])
            exit(-1)

    def send_location(self, latitude, longitude):
        headers = {'Authorization': 'Token {}'.format(self.token)}
        data = {
            'kid': self.id,
            'latitude': latitude,
            'longitude': longitude
        }
        r = requests.post(self.location_url, data=data, headers=headers)
        return r.json()

    def get_latest_location(self):
        headers = {'Authorization': 'Token {}'.format(self.token)}
        data = {
            'kid': self.id,
            'limit': 1
        }
        r = requests.get(self.location_url, params=data, headers=headers)
        return r.json()

    def send_notification(self, message):
        headers = {'Authorization': 'Token {}'.format(self.token)}
        data = {
            'kid': self.id,
            'text': message
        }
        r = requests.post(self.notification_url, data=data, headers=headers)
        return r.json()

    def move(self, lat, long):
        _meters = [0, 1, 2, 3, 4]
        meters = random.choice(_meters)
        coef = meters * 0.0000089
        step_x = random.randint(0, 1)
        if step_x == 1:
            new_lat = lat + coef
        else:
            new_lat = lat - coef
        step_y = random.randint(0, 1)
        if step_y == 1:
            new_long = long + coef / math.cos(lat * 0.018)
        else:
            new_long = long - coef / math.cos(lat * 0.018)
        return new_lat, new_long

    def walk(self):
        last_location = self.get_latest_location()['results']
        if last_location:
            last_location = last_location[0]
            lat = last_location['latitude']
            long = last_location['longitude']
        else:
            print('No initial last location found. Where is your kid now?')
            lat = get_float('Latitude: ')
            long = get_float('Longitude: ')
        while True:
            lat, long = self.move(lat, long)
            self.send_location(lat, long)
            print('Walked to: ({}, {})'.format(lat, long))
            time.sleep(3)


if __name__ == '__main__':
    username = input('Email: ')
    password = getpass()
    auth_response = authenticate(username, password)
    if 'token' not in auth_response:
        print('\n'.join(auth_response['non_field_errors']))
        exit(-1)
    kid_id = input('Kid id: ')
    kid = Kid(auth_response['token'], kid_id)
    kid.walk()


