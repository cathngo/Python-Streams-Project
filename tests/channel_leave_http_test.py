import pytest
import requests
import json
from src import config
from src.other import clear_v1
import jwt

# Checks for invalid token
def test_invalid_token_leave():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel_id = channel.json()
    #create a user
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail1@gmail.com', 'password': '122abc!@#', 'name_first': 'Tam', 'name_last': 'Lam'})
    user_token2 = user2.json()
    requests.post(config.url + 'channel/join/v2', json={'token': user_token2['token'], 'channel_id': channel_id['channel_id']})
    invalid_token = jwt.encode({'u_id': 0, 'session_id': 0}, 'Invalid', algorithm='HS256')
    leave = requests.post(config.url + 'channel/leave/v1', json={'token': invalid_token, 'channel_id': channel_id['channel_id']})
    assert leave.status_code == 403

# Checks for invalid channel
def test_invalid_channel_leave():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel_id = channel.json()
    #create a user
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail1@gmail.com', 'password': '122abc!@#', 'name_first': 'Tam', 'name_last': 'Lam'})
    user_token2 = user2.json()
    requests.post(config.url + 'channel/join/v2', json={'token': user_token2['token'], 'channel_id': channel_id['channel_id']})
    leave = requests.post(config.url + 'channel/leave/v1', json={'token': user_token2['token'], 'channel_id': channel_id['channel_id'] + 1})
    assert leave.status_code == 400


# Check if channel_leave_v1 works for member
def test_http_channel_join_works_member():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel_id = channel.json()
    #create a user
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail1@gmail.com', 'password': '122abc!@#', 'name_first': 'Tam', 'name_last': 'Lam'})
    user_token2 = user2.json()
    requests.post(config.url + 'channel/join/v2', json={'token': user_token2['token'], 'channel_id': channel_id['channel_id']})
    requests.post(config.url + 'channel/leave/v1', json={'token': user_token2['token'], 'channel_id': channel_id['channel_id']})
    #pass in channel id and token into channel details
    resp = requests.get(config.url + 'channel/details/v2', params={'token': user_token['token'], 'channel_id': channel_id['channel_id']})
    #get the response in json
    details = resp.json()
    assert len(details['all_members']) == 1

# Check if channel_leave_v1 works for owner
def test_http_channel_join_works_owner():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel_id = channel.json()
    #create a user
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail1@gmail.com', 'password': '122abc!@#', 'name_first': 'Tam', 'name_last': 'Lam'})
    user_token2 = user2.json()
    requests.post(config.url + 'channel/join/v2', json={'token': user_token2['token'], 'channel_id': channel_id['channel_id']})
    requests.post(config.url + 'channel/leave/v1', json={'token': user_token['token'], 'channel_id': channel_id['channel_id']})
    #pass in channel id and token into channel details
    resp = requests.get(config.url + 'channel/details/v2', params={'token': user_token2['token'], 'channel_id': channel_id['channel_id']})
    #get the response in json
    details = resp.json()
    assert len(details['all_members']) == 1
    assert len(details['owner_members']) == 0


# Check if user is not member of the channel
def test_http_channel_notjoined_error():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel_id = channel.json()
    #create a user
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail1@gmail.com', 'password': '122abc!@#', 'name_first': 'Tam', 'name_last': 'Lam'})
    user_token2 = user2.json()
    leave = requests.post(config.url + 'channel/leave/v1', json={'token': user_token2['token'], 'channel_id': channel_id['channel_id']})
    assert leave.status_code == 403