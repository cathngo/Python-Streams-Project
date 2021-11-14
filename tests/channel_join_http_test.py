import pytest
import requests
import json
from src import config
from src.other import clear_v1
import jwt
from src.error import AccessError, InputError


# Checks if channel is invalid and gives input error
def test_invalid_channel_id():
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
    join = requests.post(config.url + 'channel/join/v2', json={'token': user_token2['token'], 'channel_id': channel_id['channel_id'] + 1})
    assert join.status_code == InputError.code

# Check if channel_join_v2
def test_http_channel_join_works():
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
    #pass in channel id and token into channel details
    resp = requests.get(config.url + 'channel/details/v2', params={'token': user_token2['token'], 'channel_id': channel_id['channel_id']})
    #get the response in json
    details = resp.json()
    assert len(details['all_members']) == 2

# Check if user is already member of the channel
def test_http_channel_rejoin_error():
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
    join = requests.post(config.url + 'channel/join/v2', json={'token': user_token2['token'], 'channel_id': channel_id['channel_id']})
    assert join.status_code == InputError.code

# If channel is private and user is not global owner check if join is prevented
def test_http_channel_private_error():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': False})
    channel_id = channel.json()
    #create a user
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail1@gmail.com', 'password': '122abc!@#', 'name_first': 'Tam', 'name_last': 'Lam'})
    user_token2 = user2.json()
    join = requests.post(config.url + 'channel/join/v2', json={'token': user_token2['token'], 'channel_id': channel_id['channel_id']})
    assert join.status_code == AccessError.code
  

