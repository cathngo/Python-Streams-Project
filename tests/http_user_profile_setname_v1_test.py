import requests
import json
from src import config
import jwt

#check name is updated for one user
def test_name_updated_once():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    requests.put(config.url + 'user/profile/setname/v1', json={'token': user_token['token'], 'name_first': 'UpdatedFirstName', 'name_last': 'UpdatedLastName'})
    resp = requests.get(config.url + 'user/profile/v1', params={'token': user_token['token'], 'u_id': user_token['auth_user_id']})
    names = resp.json()
    assert names['name_first'] == 'UpdatedFirstName'
    assert names['name_last'] == 'UpdatedLastName'

#check name can be updated multiple times
def test_name_updated_multiples():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    requests.put(config.url + 'user/profile/setname/v1', json={'token': user_token['token'], 'name_first': 'UpdatedFirstName', 'name_last': 'UpdatedLastName'})
    requests.put(config.url + 'user/profile/setname/v1', json={'token': user_token['token'], 'name_first': 'Hailey', 'name_last': 'Moon'})
    resp = requests.get(config.url + 'user/profile/v1', params={'token': user_token['token'], 'u_id': user_token['auth_user_id']})
    names = resp.json()
    assert names['name_first'] == 'Hailey'
    assert names['name_last'] == 'Moon'

#check input error if first name less than 1 character
def test_short_first_name():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    r = requests.put(config.url + 'user/profile/setname/v1', json={'token': user_token['token'], 'name_first': '', 'name_last': 'Bean'})  
    assert r.status_code == 400

#check input error if first name less than 1 character
def test_short_last_name():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    r = requests.put(config.url + 'user/profile/setname/v1', json={'token': user_token['token'], 'name_first': 'Mister', 'name_last': ''})  
    assert r.status_code == 400

#check input error if first name than 50 characters
def test_long_first_name():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    r = requests.put(config.url + 'user/profile/setname/v1', json={'token': user_token['token'], 'name_first': 'thisNameisLongerthanfiftycharactersthisNameisLongerthanfiftycharacters', 'name_last': 'Bean'})  
    assert r.status_code == 400

#check input error if first name than 50 characters
def test_long_last_name():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    r = requests.put(config.url + 'user/profile/setname/v1', json={'token': user_token['token'], 'name_first': 'Mister', 'name_last': 'thisNameisLongerthanfiftycharactersthisNameisLongerthanfiftycharacters'})  
    assert r.status_code == 400

#access error if invalid token
def test_invalid_token():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_u_id = user_token['auth_user_id'] + 1
    invalid_token = jwt.encode({'u_id': invalid_u_id, 'session_id': 0}, config.SECRET, algorithm='HS256')
    r = requests.put(config.url + 'user/profile/setname/v1', json={'token': invalid_token, 'name_first': 'Jelly', 'name_last': 'Bean'})  
    assert r.status_code == 403   

#access error if invalid token secret
def test_invalid_token_secret():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_token = jwt.encode({'u_id': user_token['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')
    r = requests.put(config.url + 'user/profile/setname/v1', json={'token': invalid_token, 'name_first': 'Jelly', 'name_last': 'Bean'})  
    assert r.status_code == 403   

#check access error if both invalid name and invalid token
def test_invalid_name_invalid_token():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_u_id = user_token['auth_user_id'] + 1
    invalid_token = jwt.encode({'u_id': invalid_u_id, 'session_id': 0}, config.SECRET, algorithm='HS256')
    r = requests.put(config.url + 'user/profile/setname/v1', json={'token': invalid_token, 'name_first': 'thisNameisLongerthanfiftycharactersthisNameisLongerthanfiftycharacters', 'name_last': 'Bean'})  
    assert r.status_code == 403   


#check returns an empty dictionary
def test_empty_dictionary():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    resp = requests.put(config.url + 'user/profile/setname/v1', json={'token': user_token['token'], 'name_first': 'UpdatedFirstName', 'name_last': 'UpdatedLastName'})
    assert resp.json() == {}
    
#check name can be updated for least recent user
def test_name_least_recent():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    requests.post(config.url + 'auth/register/v2', json={'email': 'haileyemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Ben', 'name_last': 'Park'})
    user_token = user.json()
    requests.put(config.url + 'user/profile/setname/v1', json={'token': user_token['token'], 'name_first': 'Taco', 'name_last': 'Kebab'})
    resp = requests.get(config.url + 'user/profile/v1', params={'token': user_token['token'], 'u_id': user_token['auth_user_id']})
    names = resp.json()
    assert names['name_first'] == 'Taco'
    assert names['name_last'] == 'Kebab'