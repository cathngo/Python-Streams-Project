import requests
import json
from src import config
import jwt

#check input error if handle taken
def test_duplicate_handle():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    r1 = requests.get(config.url + 'user/profile/v1', params={'token': user_token['token'], 'u_id': user_token['auth_user_id']})
    details = r1.json()
    existing_handle = details['handle_str']
    r = requests.put(config.url + 'user/profile/sethandle/v1', json={'token': user_token['token'], 'handle_str': existing_handle})  
    assert r.status_code == 400   

#check input error if handle str > 20 characterse
def test_long_handle_str():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    r = requests.put(config.url + 'user/profile/sethandle/v1', json={'token': user_token['token'], 'handle_str': 'thisHandleIslongerthantwentyCharacters'})  
    assert r.status_code == 400

#check input error if handle str < 3 characters
def test_short_handle_str():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    r = requests.put(config.url + 'user/profile/sethandle/v1', json={'token': user_token['token'], 'handle_str': ''})  
    assert r.status_code == 400



#check input error if handle_str contains non alphanumeric characters
def test_non_alphanumeric_handle():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    r = requests.put(config.url + 'user/profile/sethandle/v1', json={'token': user_token['token'], 'handle_str': 'S&D^3nonS2±!'})  
    assert r.status_code == 400 

#check access error if invalid token for wrong u_id
def test_invalid_token():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_u_id = user_token['auth_user_id'] + 1
    invalid_token = jwt.encode({'u_id': invalid_u_id, 'session_id': 0}, config.SECRET, algorithm='HS256')
    r = requests.put(config.url + 'user/profile/sethandle/v1', json={'token': invalid_token, 'handle_str': 'UpdatedHandle'})   
    assert r.status_code == 403   

#check access error if invalid token for wrong secret
def test_invalid_token_secret():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_token = jwt.encode({'u_id': user_token['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')
    r = requests.put(config.url + 'user/profile/sethandle/v1', json={'token': invalid_token, 'handle_str': 'UpdatedHandle'})   
    assert r.status_code == 403  

#check accesserror if invalid handle and invalid token
def test_invalid_token_invalid_handle():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_u_id = user_token['auth_user_id'] + 1
    invalid_token = jwt.encode({'u_id': invalid_u_id, 'session_id': 0}, config.SECRET, algorithm='HS256')
    r = requests.put(config.url + 'user/profile/sethandle/v1', json={'token': invalid_token, 'handle_str': ''})   
    assert r.status_code == 403   
  