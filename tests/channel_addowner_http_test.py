import pytest
import requests
import json
from src import config
from src.other import clear_v1
import jwt

# Checks if the function works
def test_addowner_works():
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
    add = requests.post(config.url + 'channel/addowner/v1', json={'token': user_token['token'], 'channel_id': channel_id['channel_id'], 'u_id': user_token2['auth_user_id']})
    assert add.status_code == 200

# Checks for invalid token
def test_invalid_token_addowner():
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
    add = requests.post(config.url + 'channel/addowner/v1', json={'token': invalid_token, 'channel_id': channel_id['channel_id'], 'u_id': user_token2['auth_user_id']})
    assert add.status_code == 403

# Checks for invalid channel
def test_invalid_channel_addowner():
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
    add = requests.post(config.url + 'channel/addowner/v1', json={'token': user_token2['token'], 'channel_id': channel_id['channel_id'] + 1, 'u_id': user_token2['auth_user_id']})
    assert add.status_code == 400


# Check if u_id does not refer to a member of the channel
def test_http_channel_addowner_works_member():
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
    add = requests.post(config.url + 'channel/addowner/v1', json={'token': user_token['token'], 'channel_id': channel_id['channel_id'], 'u_id': user_token2['auth_user_id']})
    assert add.status_code == 400

# u_id refers to an owner 
def test_http_channel_addowner_already_owner():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel_id = channel.json()
    add = requests.post(config.url + 'channel/addowner/v1', json={'token': user_token['token'], 'channel_id': channel_id['channel_id'], 'u_id': user_token['auth_user_id']})
    assert add.status_code == 400


# Check if user adding is an owner
def test_http_channel_owner_adding():
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
    user3 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail2@gmail.com', 'password': '132abc!@#', 'name_first': 'Bam', 'name_last': 'Wam'})
    user_token3 = user3.json()
    requests.post(config.url + 'channel/join/v2', json={'token': user_token3['token'], 'channel_id': channel_id['channel_id']})
    add = requests.post(config.url + 'channel/addowner/v1', json={'token': user_token2['token'], 'channel_id': channel_id['channel_id'], 'u_id': user_token3['auth_user_id']})
    assert add.status_code == 403