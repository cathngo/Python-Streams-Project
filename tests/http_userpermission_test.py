import pytest
import requests
import json

from werkzeug.exceptions import UnsupportedMediaType
from src import config
import jwt


#check 
def test_adding_global_owner():
    #Reset route
    requests.delete(config.url + 'clear/v1')

    user_2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail2@gmail.com', 'password': '123abc!@#2', 'name_first': 'Masoko', 'name_last': 'West'})
    user_token2 = user_2.json()   
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'San'})
    user_token = user.json()
    user3 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail3@gmail.com', 'password': '122abc!@#2', 'name_first': 'Samor', 'name_last': 'Narco'})
    user_token3 = user3.json()
    user4 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail4@gmail.com', 'password': '122abc!@#4', 'name_first': 'Knaye', 'name_last': 'Mess'})
    user_token4 = user4.json()
    #user is the owner of this channel
    channel = requests.post(config.url + 'channels/create/v2',json={'token': user_token['token'],'name': 'Fox' , 'is_public' : True})
    channel_id = channel.json()
    #invite the other two users as normal members
    requests.post(config.url + 'channel/invite/v2',json={'token': user_token['token'],'channel_id': channel_id['channel_id'], 'u_id': user_token2['auth_user_id']})
    requests.post(config.url + 'channel/invite/v2',json={'token': user_token['token'],'channel_id': channel_id['channel_id'], 'u_id': user_token3['auth_user_id']})
    requests.post(config.url + 'channel/invite/v2',json={'token': user_token['token'],'channel_id': channel_id['channel_id'], 'u_id': user_token4['auth_user_id']})
    #promote to global owner
    requests.post(config.url + 'admin/userpermission/change/v1',json={'token': user_token2['token'] , 'u_id': user_token3['auth_user_id'], 'permission_id': 1})
    #the new global owner tries to make a new channel owner
    re = requests.post(config.url + 'channel/addowner/v1',json={'token': user_token3['token'],'channel_id': channel_id['channel_id'], 'u_id': user_token4['auth_user_id']})
    assert re.status_code == 200

def test_adding_global_owner_2():
    #Reset route
    requests.delete(config.url + 'clear/v1')

    user_2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail2@gmail.com', 'password': '123abc!@#2', 'name_first': 'Masoko', 'name_last': 'West'})
    user_token2 = user_2.json() 
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'San'})
    user_token = user.json()
    user3 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail3@gmail.com', 'password': '122abc!@#2', 'name_first': 'Samor', 'name_last': 'Narco'})
    user_token3 = user3.json()

    #user_2 (global owner) promotes user_3 to global owner
    requests.post(config.url + 'admin/userpermission/change/v1',json={'token': user_token2['token'] , 'u_id': user_token3['auth_user_id'], 'permission_id': 1})
    #user makes a channel
    channel = requests.post(config.url + 'channels/create/v2',json={'token': user_token['token'],'name': 'Fox' , 'is_public' : False})
    channel_id = channel.json()

    re = requests.post(config.url + 'channel/join/v2', json={'token': user_token2['token'], 'channel_id':channel_id['channel_id']})
    assert re.status_code == 200

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
    resp = requests.post(config.url + 'admin/userpermission/change/v1', json={'token': invalid_token, 'u_id': user_token['auth_user_id'], 'permission_id': 1})
    assert resp.status_code == 403

#check when an invalid u_id is pased 
def test_invalid_u_id_():
    requests.delete(config.url + 'clear/v1')
    #create user
    invalid_u_id = 999999
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'Chan'})
    user_token = user.json()

    #pass valid channel id but invalid token
    resp = requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user_token['token'], 'u_id': invalid_u_id, 'permission_id': 1})
    assert resp.status_code == 400

#check when the last global owner is trying to become a normal user 
def test_last_global_owner_demoted():
    requests.delete(config.url + 'clear/v1')
    #create user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'Chan'})
    user_token = user.json()

    #pass valid channel id but invalid token
    resp = requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user_token['token'], 'u_id': user_token['auth_user_id'], 'permission_id': 2})
    assert resp.status_code == 400

#check the given permision_id is not valid
def test_invalid_permision_id():
    requests.delete(config.url + 'clear/v1')
    #create user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'Chan'})
    user_token = user.json()
    user_2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail2@gmail.com', 'password': '123abc!@#2', 'name_first': 'Masoko', 'name_last': 'West'})
    user_token2 = user_2.json() 
    #create channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel.json()
    #pass valid channel id but invalid token
    resp = requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user_token['token'], 'u_id': user_token2['auth_user_id'], 'permission_id': 99})
    assert resp.status_code == 400

def test_authorised_user_not_global_owner():
    requests.delete(config.url + 'clear/v1')
    #create user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'Chan'})
    user_token = user.json()
    user_2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail2@gmail.com', 'password': '123abc!@#2', 'name_first': 'Masoko', 'name_last': 'West'})
    user_token2 = user_2.json() 
    #create channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel.json()
    #pass valid channel id but invalid token
    resp = requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user_token2['token'], 'u_id': user_token['auth_user_id'], 'permission_id': 1})
    assert resp.status_code == 403