import requests
import jwt
from src import config
from src.config import SECRET
from src.error import AccessError


# Checks if auth_logout_v2 works
def test_http_auth_logout_works():
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    payload1 = r1.json()
    r2 = requests.post(config.url + 'auth/logout/v1', json={
        'token': payload1['token'],
    })
    assert r2.status_code == 200

def test_http_auth_logout_invalid_token():
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    invalid_token = jwt.encode({'u_id': 0, 'session_id': 0}, 'Invalid', algorithm='HS256')
    r2 = requests.post(config.url + 'auth/logout/v1', json={
        'token': invalid_token,
    })
    assert r2.status_code == AccessError.code

def test_http_auth_double_logout():
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    payload1 = r1.json()
    requests.post(config.url + 'auth/logout/v1', json={
        'token': payload1['token'],
    })
    r3 = requests.post(config.url + 'auth/logout/v1', json={
        'token': payload1['token'],
    })
    assert r3.status_code == AccessError.code

def test_http_login_logout():
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    r2 = requests.post(config.url + 'auth/login/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
    })
    payload2 = r2.json()
    r3 = requests.post(config.url + 'auth/logout/v1', json={
        'token': payload2['token'],
    })
    assert r3.status_code == 200