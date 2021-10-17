import pytest
import requests
import json
from src.channels import channels_create_v1
from src.channel import channel_details_v1
from src.auth import auth_register_v1
from src import config
from src.other import clear_v1
import jwt

#check returns correct details
def test_correct_details():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel_id = channel.json()
    #pass in channel id and token into channel details
    resp = requests.get(config.url + 'channel/details/v2', params={'token': user_token['token'], 'channel_id': channel_id['channel_id']})
    #get the response in json
    details = resp.json()
    
    assert details['name'] == 'Alpaca'
    assert details['is_public'] == True
    assert details['owner_members'][0]['u_id'] == 0
    assert details['all_members'][0]['u_id'] == 0

#check acccess error for invalid id and invalid token with invalid u_id association
def test_invalid_channel_id():
    requests.delete(config.url + 'clear/v1')
    invalid_channel_id = 1000
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_u_id = user_token['auth_user_id'] + 1
    invalid_token = jwt.encode({'u_id': invalid_u_id, 'session_id': 0}, config.SECRET, algorithm='HS256')
    resp = requests.get(config.url + 'channel/details/v2', params={'token': invalid_token, 'channel_id': invalid_channel_id })
    assert resp.status_code == 403

#check access error for valid channel id and unauthorised user
def test_unauthorised_user():
    requests.delete(config.url + 'clear/v1')
    #create user and channel with token
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token1 = user1.json()
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token1['token'], 'name': 'Alpaca', 'is_public': True})
    channel_id = channel.json()
    #pass in valid channel id but invalid user
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'unauthorisedemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    unauthorised_user = user2.json()
    resp = requests.get(config.url + 'channel/details/v2', params={'token': unauthorised_user['token'], 'channel_id': channel_id['channel_id'] })
    assert resp.status_code == 403

#check input error when given invalid channel id but valid token
def test_invalid_existing_channel_id():
    requests.delete(config.url + 'clear/v1')
    #create user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel_id = channel.json()
    invalid_channel_id = channel_id['channel_id'] + 1000
    #pass in invalid channel id but valid token
    resp = requests.get(config.url + 'channel/details/v2', params={'token': user_token['token'], 'channel_id': invalid_channel_id })
    assert resp.status_code == 400

#check accesserror for invalid signature but valid channel id
def test_invalid_token_signature():
    requests.delete(config.url + 'clear/v1')
    #create user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel_id = channel.json()
    #create invalid token
    invalid_token = jwt.encode({'u_id': user_token['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')
    #pass valid channel id but invalid token
    resp = requests.get(config.url + 'channel/details/v2', params={'token': invalid_token, 'channel_id': channel_id['channel_id']})
    assert resp.status_code == 403

