import pytest
import requests
import json
from src import config
from src.other import clear_v1
import jwt

def test_invalid_channel_id_channel_messages():
    requests.delete(config.url + 'clear/v1')
    invalid_channel_id = 1000
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    resp = requests.get(config.url + 'channel/messages/v2', params={
        'token': user_token['token'],
        'channel_id': invalid_channel_id,
        'start': 0
    })
    assert resp.status_code == 400

def test_unauthorised_user_channel_messages():
    requests.delete(config.url + 'clear/v1')
    #create user and channel with token
    user1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token1 = user1.json()
    
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_token1['token'],
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id = channel.json()
    #pass in valid channel id but invalid user
    user2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'unauthorisedemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    unauthorised_user = user2.json()
    resp = requests.get(config.url + 'channel/details/v2', params={
        'token': unauthorised_user['token'], 
        'channel_id': channel_id['channel_id'],
        'start': 0
    })
    assert resp.status_code == 403

def test_invalid_token_signature_channel_messages():
    requests.delete(config.url + 'clear/v1')
    #create user
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    #create channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_token['token'], 
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id = channel.json()
    #create invalid token
    invalid_token = jwt.encode({'u_id': user_token['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')
    #pass valid channel id but invalid token
    resp = requests.get(config.url + 'channel/messages/v2', params={
        'token': invalid_token, 
        'channel_id': channel_id['channel_id'],
        'start': 0
    })
    assert resp.status_code == 403

def test_channel_messages_route_works():
    requests.delete(config.url + 'clear/v1')
     #create a user
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_token['token'], 
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id = channel.json()
    #pass in a start that is greater to the number of messages in the system
    resp = requests.get(config.url + 'channel/messages/v2', params={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'start': 0,
    })
    #get the response in json
    assert resp.status_code == 200

#tests that there is a negative one when the end of a message is reached
def test_negative_one_end_of_messages_channel_messages():
    requests.delete(config.url + 'clear/v1')
     #create a user
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_token['token'], 
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id = channel.json()
    #pass in start when there are no more messages
    resp = requests.get(config.url + 'channel/messages/v2', params={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'start': 0,
    })
    #get the response in json
    messages = resp.json()
    assert messages['end'] == -1


def test_start_greater_than_messages_channel_messages():
    requests.delete(config.url + 'clear/v1')
     #create a user
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_token['token'], 
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id = channel.json()
    #pass in a start that is greater to the number of messages in the system
    resp = requests.get(config.url + 'channel/messages/v2', params={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'start': 1,
    })
    #get the response in json
    assert resp.status_code == 400

