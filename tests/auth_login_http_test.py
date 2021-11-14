import requests
import jwt
from src import config
from src.config import SECRET
from src.error import InputError



# Checks if auth_login_v2 works correctly 
def test_http_auth_login_works():
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    payload1 = r1.json()
    user1_info = jwt.decode(payload1['token'], SECRET, algorithms=['HS256'])
    r2 = requests.post(config.url + 'auth/login/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
    })
    payload2 = r2.json()
    user2_info = jwt.decode(payload2['token'], SECRET, algorithms=['HS256'])
    assert user1_info['u_id'] == user2_info['u_id']


# Check if email entered does not belong to a user 
def test_http_unregistered_auth_login():
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    r2 = requests.post(config.url + 'auth/login/v2', json={
        'email': 'user2@email.com',
        'password': 'user2password',
    })
    assert r2.status_code == InputError.code

# Check if email entered is not a valid email
def test_http_invalid_email_auth_login():
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    r2 = requests.post(config.url + 'auth/login/v2', json={
        'email': '',
        'password': 'user2password',
    })
    assert r2.status_code == InputError.code

# Check if password is not correct
def test_http_auth_login_incorrect_password():
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    r2 = requests.post(config.url + 'auth/login/v2', json={
        'email': 'user1@email.com',
        'password': 'user2password',
    })
    assert r2.status_code == InputError.code
    
    
    
