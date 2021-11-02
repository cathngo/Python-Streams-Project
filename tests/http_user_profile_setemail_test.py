import requests
import json
from src import config
import jwt

#check input error email not valid
def test_invalid_email():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    r = requests.put(config.url + 'user/profile/setemail/v1', json={'token': user_token['token'], 'email': 'bademail.com'})  
    assert r.status_code == 400

#check input error for dupilicate email
def test_duplicate_email():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'duplicateemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    r = requests.put(config.url + 'user/profile/setemail/v1', json={'token': user_token['token'], 'email': 'duplicateemail@gmail.com'})  
    assert r.status_code == 400

#check access error for invalid token decoded with invalid secret
def test_invalid_token():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_u_id = user_token['auth_user_id'] + 1
    invalid_token = jwt.encode({'u_id': invalid_u_id, 'session_id': 0}, config.SECRET, algorithm='HS256')
    r = requests.put(config.url + 'user/profile/setemail/v1', json={'token': invalid_token, 'email': 'validemail@gmail.com'})   
    assert r.status_code == 403   

#check access error for invalid token decoded with invalid u_id
def test_invalid_token_secret():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_token = jwt.encode({'u_id': user_token['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')
    r = requests.put(config.url + 'user/profile/setemail/v1', json={'token': invalid_token, 'email': 'validemail@gmail.com'})   
    assert r.status_code == 403  

#check access error for BOTH invalid email format and invalid token
def test_invalid_email_invalid_token():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_token = jwt.encode({'u_id': user_token['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')
    r = requests.put(config.url + 'user/profile/setemail/v1', json={'token': invalid_token, 'email': 'bademail.com'})   
    assert r.status_code == 403  

#check access error for BOTH invalid duplicate email and invalid token
def test_duplicate_email_invalid_token():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_token = jwt.encode({'u_id': user_token['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')
    r = requests.put(config.url + 'user/profile/setemail/v1', json={'token': invalid_token, 'email': 'validemail@gmail.com'})   
    assert r.status_code == 403  

#check email successfully updated for multiple cases
def test_update_email():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'anotheremail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kelly', 'name_last': 'River'})
    user1_token = user1.json()
    user2_token = user2.json()
    requests.put(config.url + 'user/profile/setemail/v1', json={'token': user1_token['token'], 'email': 'SamNewemail@gmail.com'})   
    requests.put(config.url + 'user/profile/setemail/v1', json={'token': user2_token['token'], 'email': 'KellyNewemail@gmail.com'})   
    r1 = requests.get(config.url + 'user/profile/v1', params={'token': user1_token['token'], 'u_id': user1_token['auth_user_id']})
    r2 = requests.get(config.url + 'user/profile/v1', params={'token': user2_token['token'], 'u_id': user2_token['auth_user_id']})
    email1 = r1.json()
    email2 = r2.json()
    assert email1['user']['email'] =='SamNewemail@gmail.com'
    assert email2['user']['email'] == 'KellyNewemail@gmail.com'

#check email successfuly updated for the same user
def test_multiple_update():
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    requests.put(config.url + 'user/profile/setemail/v1', json={'token': user_token['token'], 'email': 'first@gmail.com'})   
    requests.put(config.url + 'user/profile/setemail/v1', json={'token': user_token['token'], 'email': 'second@gmail.com'})   
    r1 = requests.get(config.url + 'user/profile/v1', params={'token': user_token['token'], 'u_id': user_token['auth_user_id']})
    email1 = r1.json()
    assert email1['user']['email'] =='second@gmail.com'


#check successfullly updates the least recent  user
def test_least_recent():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    requests.post(config.url + 'auth/register/v2', json={'email': 'anotheremail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kelly', 'name_last': 'River'})
    user1_token = user1.json()
    requests.put(config.url + 'user/profile/setemail/v1', json={'token': user1_token['token'], 'email': 'leastrecent@gmail.com'})   
    r1 = requests.get(config.url + 'user/profile/v1', params={'token': user1_token['token'], 'u_id': user1_token['auth_user_id']})
    payload = r1.json()
    assert payload['user']['email'] == 'leastrecent@gmail.com'