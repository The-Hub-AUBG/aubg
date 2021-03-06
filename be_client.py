from uuid import uuid4

import requests
import json
import datetime

class SomethingWayClient:
    def __init__(self):
        self.HOST = 'http://www.somethingway.com'
        self.AuthRegister = '/auth/register'
        self.AuthLogin = '/auth/login'
        self.AuthLogout = '/auth/logout'
        self.Devices = '/customer/{}/devices'  # methods=['GET', 'POST']
        self.DeviceSingle = '/customer/<customer_id>/devices/<device_id>'  # methods=['GET', 'PATCH', 'DELETE']
        self.DeviceDataFetch = '/customer/<customer_id>/devices/<device_id>/fetch/'  # methods=['POST']
        self.DeviceDataStore = '/customer/<customer_id>/devices/<device_id>/store/'  # methods=['POST']
        self.auth_token = None
        self.headers = None

    def register(self, request_body):
        response = requests.post(self.HOST + self.AuthRegister, json=request_body)

    def login(self, request_body):
        response = requests.post(self.HOST + self.AuthLogin, request_body)
        resp = json.loads(response.content)
        self.auth_token = resp.get('auth_token', None)
        if not self.auth_token:
            raise Exception("The login did not return token.")
        self.headers = {
            "Authorization": self.auth_token
        }

    def register_device(self):
        request_body = {
            "name": "AuraRGBModule1",
            "description": "Static Aura Slavov1",
            "geolocation_data": {
                "lon": 43.1234,
                "lat": 24.5678
            },
            "device_id": "staticaura",
        }
        response = requests.post(self.HOST + "/customer/603af10ba4d8ecdf1a0438df/devices", json=request_body, headers=self.headers)

    def store_data(self, sensor_data):
        request_body = {
            'TS': str(datetime.datetime.now().timestamp()).split('.')[0],
            **sensor_data,
        }

        response = requests.post(self.HOST + "/customer/603af10ba4d8ecdf1a0438df/devices/staticaura/store", json=request_body, headers=self.headers)


    def fetch(self):
        request_body = {
            "from": str((datetime.datetime.now()-datetime.timedelta(minutes=1)).timestamp()).split('.')[0],
            "to": str(datetime.datetime.now().timestamp()).split('.')[0]
        }
        response = requests.post(self.HOST + "/customer/603af10ba4d8ecdf1a0438df/devices/staticaura/fetch", json=request_body, headers=self.headers)

        return json.loads(response.content)


if __name__ == '__main__':
    cli = SomethingWayClient()

    creds = {
        "email": "kostadin@slavov.net",
        "password": "verysecure",

    }

    cli.login(creds)
    user_uid = "603af10ba4d8ecdf1a0438df"
    # cli.register_device()
    for i in range(1000):
        cli.store_data()
        cli.fetch()
        print(i)
