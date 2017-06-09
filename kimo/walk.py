import requests
from requests import exceptions
from getpass import getpass
import time
import random
import math


def retry(report=lambda *args: None):
    def wrapper(fnc):
        def wrapped(*args, **kwargs):
            while True:
                try:
                    return fnc(*args, **kwargs)
                except requests.exceptions.HTTPError as problem:
                    report('Failed with {}. Sleeping 5 seconds'.format(problem))
                except ConnectionRefusedError as problem:
                    report('Failed with {}. Sleeping 5 seconds'.format(problem))
                    time.sleep(5)
                except (ConnectionAbortedError, ConnectionResetError) as problem:
                    report('Failed with {}. Sleeping 10 seconds'.format(problem))
                except ConnectionError as problem:
                    report('Failed with {}. Sleeping 30 seconds'.format(problem))
                except Exception as exc:
                    report('Failed with uncaught error: {}. Quiting.'.format(exc))
                    break
        return wrapped
    return wrapper


@retry(print)
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
    R = 6371e3
    phi_1 = math.radians(coord_1[0])
    phi_2 = math.radians(coord_2[0])

    delta_phi = math.radians(coord_2[0] - coord_1[0])
    delta_lambda = math.radians(coord_2[1] - coord_1[1])

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c


def generate_out_of_bounds(name):
    return '{} has gone out of the restricted area.'.format(name)


def generate_collision(name):
    message = '{} was hit by a {}'
    possibilities = ['car', 'bus', 'bicycle', 'nuke', 'drone']

    return message.format(name, random.choice(possibilities))


def move(lat, long):
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


class Kid(object):
    def __init__(self, token, kid_id):
        self.token = token
        self.id = kid_id
        self.location_url = 'http://127.0.0.1/api/location/'
        self.notification_url = 'http://127.0.0.1/api/notification/'
        self.restriction_url = 'http://127.0.0.1/api/restriction/'
        self.weather_link = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=meters'
        self.kid_url = 'http://127.0.0.1/api/kid/{}'.format(self.id)
        self.name = self.check_kid_resource()
        self.out_of_bounds = False

    @retry(print)
    def check_kid_resource(self):
        headers = {'Authorization': 'Token {}'.format(self.token)}
        response = requests.get(self.kid_url, headers=headers).json()
        if 'detail' in response:
            print(response['detail'])
            exit(-1)
        return response['first_name']

    @retry(print)
    def send_location(self, latitude, longitude):
        headers = {'Authorization': 'Token {}'.format(self.token)}
        data = {
            'kid': self.id,
            'latitude': latitude,
            'longitude': longitude
        }
        r = requests.post(self.location_url, data=data, headers=headers)
        return r.json()

    @retry(print)
    def get_latest_location(self):
        headers = {'Authorization': 'Token {}'.format(self.token)}
        data = {
            'kid': self.id,
            'limit': 1
        }
        r = requests.get(self.location_url, params=data, headers=headers)
        return r.json()

    @retry(print)
    def send_notification(self, message, _type):
        headers = {'Authorization': 'Token {}'.format(self.token)}
        data = {
            'kid': self.id,
            'text': message,
            'type': _type
        }
        r = requests.post(self.notification_url, data=data, headers=headers)
        return r.json()

    @retry(print)
    def check_out_of_bounds(self, latitude, longitude):
        headers = {'Authorization': 'Token {}'.format(self.token)}
        data = {
            'kid': self.id
        }
        r = requests.get(self.restriction_url, params=data, headers=headers).json()
        next_page = True
        self.out_of_bounds = True
        while next_page:
            if not r['next']:
                next_page = False
            for data in r['results']:
                distance = compute_distance((latitude, longitude), (data['latitude'], data['longitude']))
                print(distance)
                if distance <= data['distance']:
                    self.out_of_bounds = False
                    break
            if not self.out_of_bounds:
                break
            r = requests.get(self.restriction_url, params=data, headers=headers).json()

    @retry(print)
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
            lat, long = move(lat, long)
            self.send_location(lat, long)
            print('Walked to: ({}, {})'.format(lat, long))
            out_of_bounds = self.out_of_bounds
            self.check_out_of_bounds(lat, long)
            if self.out_of_bounds and not out_of_bounds:
                self.send_notification(generate_out_of_bounds(self.name), 'out_of_bounds')
            collision = random.random()
            if collision <= 0.001:
                self.send_notification(generate_collision(self.name), 'collision')
            time.sleep(3)


if __name__ == '__main__':
    username = input('Email: ')
    password = getpass()
    auth_response = authenticate(username, password)
    if auth_response and 'token' not in auth_response:
        print('\n'.join(auth_response['non_field_errors']))
        exit(-1)
    elif not auth_response:
        exit(-1)
    kid_id = input('Kid id: ')
    kid = Kid(auth_response['token'], kid_id)
    kid.walk()


