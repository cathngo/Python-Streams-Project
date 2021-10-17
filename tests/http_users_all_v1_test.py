import pytest
import requests
import json
from src import config
from src.other import clear_v1
import jwt

#check returns correct user details
def test_correct_user_details():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #get token from auth reg
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    resp = requests.get(config.url + 'users/all/v1', params={'token': user_token['token']})
    r = resp.json()
    assert r['name_first'] == 'Sam'
    assert r['name_last'] == 'Smith'
    assert r['email'] == 'validemail@gmail.com'

#check returns correct user with multiple existing users
def test_multiple_users():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #get token from auth reg
    requests.post(config.url + 'auth/register/v2', json={'email': 'validemail1@gmail.com', 'password': '123abc!@#', 'name_first': 'Kelly', 'name_last': 'Swan'})
    requests.post(config.url + 'auth/register/v2', json={'email': 'validemail2@gmail.com', 'password': '123abc2!@#', 'name_first': 'Donut', 'name_last': 'King'})
    requests.post(config.url + 'auth/register/v2', json={'email': 'validemail3@gmail.com', 'password': '123abc3!@#', 'name_first': 'Sean', 'name_last': 'Ocean'})
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail4@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    resp = requests.get(config.url + 'users/all/v1', params={'token': user_token['token']})
    r = resp.json()
    assert r['name_first'] == 'Sam'
    assert r['name_last'] == 'Smith'
    assert r['email'] == 'validemail@gmail.com'

#check accesserror for invalid token for invalid user
def test_invalid_token():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_u_id = user_token['auth_user_id'] + 1
    invalid_token = jwt.encode({'u_id': invalid_u_id, 'session_id': 0}, config.SECRET, algorithm='HS256')
    resp = requests.get(config.url + 'users/all/v1', params={'token': invalid_token})
    r = resp.json()
    assert r.status_code == 403

#check accesserror for token with wrong secret
def test_invalid_secret():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_token = jwt.encode({'u_id': user_token['auth_user_id'], 'session_id': 0}, config.SECRET, algorithm='HS256')
    resp = requests.get(config.url + 'users/all/v1', params={'token': invalid_token})
    r = resp.json()
    assert r.status_code == 403