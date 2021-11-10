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

#check the return list of users/all
def test_user_all_remove():
    requests.delete(config.url + 'clear/v1')
    #create users
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'Chan'})
    user_token = user.json()
    user_2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail2@gmail.com', 'password': '123abc!@#2', 'name_first': 'Masoko', 'name_last': 'West'})
    user_token2 = user_2.json() 
    #remove the second user
    requests.delete(config.url + 'admin/user/remove/v1', json={'token': user_token['token'], 'u_id':user_token2['auth_user_id']})
    #return list of all users without the removed ones
    users_dc = requests.get(config.url + 'users/all/v1', params={'token': user_token['token']})
    users_list = users_dc.json()

    assert len(users_list['users']) == 1

#check when the last global owner tries to remove himself
def test_remove_last_global_owner():
    requests.delete(config.url + 'clear/v1')
    #create users
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'Chan'})
    user_token = user.json()
    re = requests.delete(config.url + 'admin/user/remove/v1', json={'token': user_token['token'], 'u_id':user_token['auth_user_id']})
    assert re.status_code == 400

#normal member tries to remove other members
def test_not_authorised_removes():
    requests.delete(config.url + 'clear/v1')
    #create users
    requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'Chan'})
    user_2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail2@gmail.com', 'password': '123abc!@#2', 'name_first': 'Masoko', 'name_last': 'West'})
    user_token2 = user_2.json() 
    user3 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail3@gmail.com', 'password': '122abc!@#2', 'name_first': 'Samor', 'name_last': 'Narco'})
    user_token3 = user3.json()
    #user2 who is not a global owner tries to remove another member 
    re = requests.delete(config.url + 'admin/user/remove/v1', json={'token': user_token2['token'], 'u_id':user_token3['auth_user_id']})
    assert re.status_code == 403

#global owner removes channel owner from streams
def test_removed_channel_owner():
    requests.delete(config.url + 'clear/v1')
    #create users
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'Chan'})
    user_token = user.json()
    user_2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail2@gmail.com', 'password': '123abc!@#2', 'name_first': 'Masoko', 'name_last': 'West'})
    user_token2 = user_2.json() 
    user3 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail3@gmail.com', 'password': '122abc!@#2', 'name_first': 'Samor', 'name_last': 'Narco'})
    user_token3 = user3.json()

    #user2 is the owner of this channel
    channel = requests.post(config.url + 'channels/create/v2',json={'token': user_token2['token'],'name': 'Fox' , 'is_public' : True})
    channel_id = channel.json()
    #global owner removes user2
    r = requests.delete(config.url + 'admin/user/remove/v1', json={'token': user_token['token'], 'u_id':user_token2['auth_user_id']})
    assert r.status_code == 200
    #deleted user2 invites another user to the channel made by user2
    re = requests.post(config.url + 'channel/invite/v2',json={'token': user_token2['token'],'channel_id': channel_id['channel_id'], 'u_id': user_token3['auth_user_id']})
    assert re.status_code == 403

#check user profile
def test_remove_and_check_profile():
    requests.delete(config.url + 'clear/v1')
    #create users
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'Chan'})
    user_token = user.json()
    user_2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail2@gmail.com', 'password': '123abc!@#2', 'name_first': 'Masoko', 'name_last': 'West'})
    user_token2 = user_2.json() 

    requests.delete(config.url + 'admin/user/remove/v1', json={'token': user_token['token'], 'u_id':user_token2['auth_user_id']})

    #check profile details
    resp = requests.get(config.url + 'user/profile/v1', params={'token': user_token['token'], 'u_id': user_token2['auth_user_id']})
    r = resp.json()
    assert resp.status_code == 200
    assert r['user']['name_first'] == 'Removed'
    assert r['user']['name_last'] == 'user'
    assert r['user']['email'] == ''
    

#remove an user and try to registed another user with the same email as the removed user
def test_reusable_email():
    requests.delete(config.url + 'clear/v1')
    #create users
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'Chan'})
    user_token = user.json()
    user_2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail2@gmail.com', 'password': '123abc!@#2', 'name_first': 'Masoko', 'name_last': 'West'})
    user_token2 = user_2.json() 

    requests.delete(config.url + 'admin/user/remove/v1', json={'token': user_token['token'], 'u_id':user_token2['auth_user_id']})
    #reuse the email
    user3 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail2@gmail.com', 'password': '122abc!@#2', 'name_first': 'Masoko', 'name_last': 'West'})
    assert user3.status_code == 200

#normal uses creates dm and the user is removed by a global owner
def test_remove_dm_owner():
    requests.delete(config.url + 'clear/v1')
    #create users
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'Chan'})
    user_token = user.json()
    user_2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail2@gmail.com', 'password': '123abc!@#2', 'name_first': 'Masoko', 'name_last': 'West'})
    user_token2 = user_2.json() 
    #user2 creates dm
    dm_i = requests.post(config.url + 'dm/create/v1', json={'token': user_token2['token'],'u_ids': [user_token['auth_user_id']]})
    dm_id = dm_i.json()
    #remove user2
    requests.delete(config.url + 'admin/user/remove/v1', json={'token': user_token['token'], 'u_id':user_token2['auth_user_id']})

    re = requests.post(config.url + 'dm/leave/v1', json={'token': user_token2['token'], 'dm_id': dm_id['dm_id']})
    assert re.status_code == 403

#test removing user with dm messages and channel messages 
def test_remove_messages_owner():
    requests.delete(config.url + 'clear/v1')
    #create users
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'Chan'})
    user_token = user.json()
    user_2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail2@gmail.com', 'password': '123abc!@#2', 'name_first': 'Masoko', 'name_last': 'West'})
    user_token2 = user_2.json() 

    #user2 creates channel
    channel = requests.post(config.url + 'channels/create/v2',json={'token': user_token2['token'],'name': 'Fox' , 'is_public' : True})
    channel_id = channel.json()
    #user2 creates dm
    dm_i = requests.post(config.url + 'dm/create/v1', json={'token': user_token2['token'],'u_ids': [user_token['auth_user_id']]})
    dm_id = dm_i.json()

    requests.post(config.url + 'message/senddm/v1', json={'token': user_token2['token'], 'dm_id': dm_id['dm_id'],'message': "hello"})
    requests.post(config.url + 'message/send/v1', json={'token': user_token2['token'], 'channel_id': channel_id['channel_id'],'message': "hello"})
    #remove user2
    re = requests.delete(config.url + 'admin/user/remove/v1', json={'token': user_token['token'], 'u_id':user_token2['auth_user_id']})
    assert re.status_code == 200
