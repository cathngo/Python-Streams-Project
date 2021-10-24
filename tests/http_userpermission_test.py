import pytest
import requests
import json
from src import config
import jwt


#check 
def test_adding_new_admi():
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

def test_invalid_u_id_():
    #Reset route
    requests.delete(config.url + 'clear/v1')

    user_2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail2@gmail.com', 'password': '123abc!@#2', 'name_first': 'Masoko', 'name_last': 'West'})
    user_token2 = user_2.json() 