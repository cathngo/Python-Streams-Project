import pytest
import requests
import json
from src import config
from src.other import clear_v1
import jwt
from src.error import AccessError, InputError

# Checks if the function works
def test_removeowner_works():
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
    requests.post(config.url + 'channel/addowner/v1', json={'token': user_token['token'], 'channel_id': channel_id['channel_id'], 'u_id': user_token2['auth_user_id']})
    remove = requests.post(config.url + 'channel/removeowner/v1', json={'token': user_token['token'], 'channel_id': channel_id['channel_id'], 'u_id': user_token2['auth_user_id']})
    assert remove.status_code == 200

# Checks for invalid token
def test_invalid_token_removeowner():
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
    requests.post(config.url + 'channel/addowner/v1', json={'token': user_token['token'], 'channel_id': channel_id['channel_id'], 'u_id': user_token2['auth_user_id']})
    invalid_token = jwt.encode({'u_id': 0, 'session_id': 0}, 'Invalid', algorithm='HS256')
    remove = requests.post(config.url + 'channel/removeowner/v1', json={'token': invalid_token, 'channel_id': channel_id['channel_id'], 'u_id': user_token2['auth_user_id']})
    assert remove.status_code == AccessError.code

# Checks for invalid channel
def test_invalid_channel_removeowner():
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
    requests.post(config.url + 'channel/addowner/v1', json={'token': user_token2['token'], 'channel_id': channel_id['channel_id'], 'u_id': user_token2['auth_user_id']})
    remove = requests.post(config.url + 'channel/removeowner/v1', json={'token': user_token2['token'], 'channel_id': channel_id['channel_id'] + 1, 'u_id': user_token['auth_user_id']})
    assert remove.status_code == InputError.code


# Check if u_id does not refer to an owner of a channel
def test_http_channel_removeowner_works_member():
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
    remove = requests.post(config.url + 'channel/removeowner/v1', json={'token': user_token['token'], 'channel_id': channel_id['channel_id'], 'u_id': user_token2['auth_user_id']})
    assert remove.status_code == InputError.code

# u_id refers to a user who is currently the only owner of the channel
def test_http_channel_removeowner_already_owner():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel_id = channel.json()
    remove = requests.post(config.url + 'channel/removeowner/v1', json={'token': user_token['token'], 'channel_id': channel_id['channel_id'], 'u_id': user_token['auth_user_id']})
    assert remove.status_code == InputError.code


# Channel_id is valid and the authorised user does not have owner permissions in the channel
def test_http_channel_owner_removing():
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
    remove = requests.post(config.url + 'channel/removeowner/v1', json={'token': user_token2['token'], 'channel_id': channel_id['channel_id'], 'u_id': user_token['auth_user_id']})
    assert remove.status_code == AccessError.code

# Remove owner from 2nd channel
def test_remove_owner_second_channel_works():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create 2 channels with that user
    requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Hello', 'is_public': True})
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel_id = channel.json()
    #create a user
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail1@gmail.com', 'password': '122abc!@#', 'name_first': 'Tam', 'name_last': 'Lam'})
    user_token2 = user2.json()
    requests.post(config.url + 'channel/join/v2', json={'token': user_token2['token'], 'channel_id': channel_id['channel_id']})
    requests.post(config.url + 'channel/addowner/v1', json={'token': user_token['token'], 'channel_id': channel_id['channel_id'], 'u_id': user_token2['auth_user_id']})
    remove = requests.post(config.url + 'channel/removeowner/v1', json={'token': user_token['token'], 'channel_id': channel_id['channel_id'], 'u_id': user_token2['auth_user_id']})
    assert remove.status_code == 200