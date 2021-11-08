import requests
import json
from src import config
import jwt

def test_send_email():
    re = requests.post(config.url + 'auth/passwordreset/request/v1', json={'email': 'alpacatesting123@gmail.com'})
    assert re.status_code == 200
