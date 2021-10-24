import pytest
import requests
import json

from werkzeug.exceptions import UnsupportedMediaType
from src import config
import jwt 


#check if the token is valid
def test_token_is_invalid():
    requests.delete(config.url + 'clear/v1')
    #create user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'Chan'})
    user_token = user.json()
    #create channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel.json()
    #create invalid token
    invalid_token = jwt.encode({'u_id': user_token['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')
    #pass valid channel id but invalid token
    resp = requests.delete(config.url + 'admin/user/remove/v1', json={'token': invalid_token, 'u_id': user_token['auth_user_id']})
    assert resp.status_code == 403

#check when u_id is invalid
def test_remove_invalid_u_id():
    requests.delete(config.url + 'clear/v1')
    #create user
    invalid_u_id = 99
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'Kami'})
    user_token = user.json()

    #pass valid channel id but invalid token
    resp = requests.delete(config.url + 'admin/user/remove/v1', json={'token': user_token['token'], 'u_id': invalid_u_id})
    assert resp.status_code == 400

