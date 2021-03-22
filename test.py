import json
import os
import unittest

import requests

from multiprocessing import Process

from app import ItemExchange
from db import db

app = ItemExchange(db)
port = 5000


def run_server():
    app.start(port)


t = Process(target=run_server)


class TestLoginFlow(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        file_name = 'object-collection.db'
        if os.path.isfile(file_name):
            os.remove(file_name)
        import time
        t.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls) -> None:
        file_name = 'object-collection.db'
        if os.path.isfile(file_name):
            os.remove(file_name)
        t.kill()
        t.join()

    def test_registration(self):
        # given
        url = "http://localhost:{0}/register".format(port)
        data = {'login': 'Alice', 'password': '1234'}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)

        # then
        self.assertEqual(201, r.status_code)
        self.assertEqual(r.json()['message'], 'User created successfully.')

    def test_registration_empty_login(self):
        # given
        url = "http://localhost:{0}/register".format(port)
        data = {'login': '', 'password': '1234'}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)

        # then
        self.assertEqual(400, r.status_code)
        self.assertEqual(r.json()['message'], 'The login cannot be left blank!')

    def test_registration_empty_password(self):
        # given
        url = "http://localhost:{0}/register".format(port)
        data = {'login': 'sdfsdf', 'password': ''}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)

        # then
        self.assertEqual(400, r.status_code)
        self.assertEqual(r.json()['message'], 'The password cannot be left blank!')

    def test_login(self):
        # given
        url = "http://localhost:{0}/login".format(port)
        data = {'login': 'Alice', 'password': '1234'}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)

        # then
        self.assertEqual(200, r.status_code)

if __name__ == '__main__':
    unittest.main()
