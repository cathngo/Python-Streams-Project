import pytest
import requests
import json
from src import config
from src.other import clear_v1
import jwt
from src.error import AccessError, InputError

#check returns channel id if valid channel
def test_successful_channel_id():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #get token from auth reg
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    resp = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    r = resp.json()
    assert len(r) == 1

#check returns a unique channel_id
def test_unique_channel_id():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    resp_one = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    resp_two = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Llama', 'is_public': True})
    first_channel = resp_one.json()
    second_channel = resp_two.json()
    assert first_channel['channel_id'] != second_channel['channel_id']

#check if name is greater than 20 characters
def test_long_name():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    resp = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'nameLongerThanTwentyCharacter', 'is_public': True})
    assert resp.status_code == InputError.code

#check if name is less than 1
def test_short_name():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    resp = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': '', 'is_public': True})
    assert resp.status_code == InputError.code

#check accesserror for invalid token for invalid signature
def test_invalid_token_signature():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_u_id = user_token['auth_user_id'] + 1
    invalid_token = jwt.encode({'u_id': invalid_u_id, 'session_id': 0}, 'Invalid', algorithm='HS256')
    resp = requests.post(config.url + 'channels/create/v2', json={'token': invalid_token, 'name': 'Alpaca', 'is_public': True})
    #asset status code is access error 
    assert resp.status_code == AccessError.code

#check accesserror for invalid token given invalid id
def test_invalid_token():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_u_id = user_token['auth_user_id'] + 1
    invalid_token = jwt.encode({'u_id': invalid_u_id, 'session_id': 0}, config.SECRET, algorithm='HS256')
    resp = requests.post(config.url + 'channels/create/v2', json={'token': invalid_token, 'name': 'Alpaca', 'is_public': True})
    #asset status code is access error 
    assert resp.status_code == AccessError.code


