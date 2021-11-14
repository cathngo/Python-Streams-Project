import pytest
import requests
import json
from src import config
import jwt
from src.error import AccessError, InputError

#check input error when for invalid u_id but valid token
def test_invalid_u_id():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #get token from auth reg
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_u_id = user_token['auth_user_id'] + 100
    resp = requests.get(config.url + 'user/profile/v1', params={'token': user_token['token'], 'u_id': invalid_u_id})
    resp.status_code == InputError.code

#check returns correct details
def test_correct_details():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #get token from auth reg
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    resp = requests.get(config.url + 'user/profile/v1', params={'token': user_token['token'], 'u_id': user_token['auth_user_id']})
    r = resp.json()
    assert r['user']['name_first'] == 'Sam'
    assert r['user']['name_last'] == 'Smith'
    assert r['user']['email'] == 'validemail@gmail.com'
    assert r['user']['u_id'] == user_token['auth_user_id']

#check returns correct user details given multiple users registered
def test_multiple_users():
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json={'email': 'validemail1@gmail.com', 'password': '123abc!@#', 'name_first': 'Kelly', 'name_last': 'Swan'})
    token = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail2@gmail.com', 'password': '123abc2!@#', 'name_first': 'Donut', 'name_last': 'King'})
    user2= token.json()
    requests.post(config.url + 'auth/register/v2', json={'email': 'validemail3@gmail.com', 'password': '123abc3!@#', 'name_first': 'Sean', 'name_last': 'Ocean'})
    resp = requests.get(config.url + 'user/profile/v1', params={'token': user2['token'], 'u_id': user2['auth_user_id']})
    r = resp.json()
    assert r['user']['name_first'] == 'Donut'
    assert r['user']['name_last'] == 'King'
    assert r['user']['email'] == 'validemail2@gmail.com'
    assert r['user']['u_id'] == user2['auth_user_id']

#check accesserror for BOTH invalid token and invalid u_id
def test_invalid_token():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_u_id = user_token['auth_user_id'] + 1
    invalid_token = jwt.encode({'u_id': invalid_u_id, 'session_id': 0}, config.SECRET, algorithm='HS256')
    resp = requests.get(config.url + 'user/profile/v1', params={'token': invalid_token, 'u_id': invalid_u_id})
    assert resp.status_code == AccessError.code

#check accesserror for token with wrong secret
def test_invalid_secret():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_token = jwt.encode({'u_id': user_token['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')
    resp = requests.get(config.url + 'user/profile/v1', params={'token': invalid_token, 'u_id': user_token['auth_user_id']})
    assert resp.status_code == AccessError.code

#check access error for invalid token but valid id
def test_invalid_token_valid_u_id():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_u_id = user_token['auth_user_id'] + 1
    invalid_token = jwt.encode({'u_id': invalid_u_id, 'session_id': 0}, config.SECRET, algorithm='HS256')
    resp = requests.get(config.url + 'user/profile/v1', params={'token': invalid_token, 'u_id': user_token['auth_user_id']})
    assert resp.status_code == AccessError.code
