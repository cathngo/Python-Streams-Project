import time
import pytest
import requests
import json
from datetime import datetime
from src import config
from src.other import clear_v1
import jwt
from src.error import InputError, AccessError


def test_invalid_channel_id_message_send_later():
    requests.delete(config.url + 'clear/v1')
    invalid_channel_id = 1000
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    resp = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user_token['token'],
        'channel_id': invalid_channel_id,
        'message': "hello",
        'time_sent': int(datetime.now().timestamp()) + 5,
        'is_pinned': False,
        'reacts':[
                {
                    'react_id': 1,
                    'u_ids': [], 
                    'is_this_user_reacted': False
                }
            ]
    })
    assert resp.status_code == InputError.code

def test_unauthorised_user_message_send_later():
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
    resp = requests.post(config.url + 'message/sendlater/v1', json={
        'token': unauthorised_user['token'], 
        'channel_id': channel_id['channel_id'],
        'message': "hello",
        'time_sent': int(datetime.now().timestamp()) + 5,
        'is_pinned': False,
        'reacts':[
                {
                    'react_id': 1,
                    'u_ids': [], 
                    'is_this_user_reacted': False
                }
            ]
    })
    assert resp.status_code == AccessError.code

def test_invalid_token_signature_message_send_later():
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
    resp = requests.post(config.url + 'message/sendlater/v1', json={
        'token': invalid_token, 
        'channel_id': channel_id['channel_id'],
        'message': "hello",
        'time_sent': int(datetime.now().timestamp()) + 5,
        'is_pinned': False,
        'reacts':[
                {
                    'react_id': 1,
                    'u_ids': [], 
                    'is_this_user_reacted': False
                }
            ]
    })
    assert resp.status_code == AccessError.code

def test_route_works_message_send_later():
    requests.delete(config.url + 'clear/v1')

    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()

    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_token['token'], 
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id = channel.json()

    resp = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'message': "hello",
        'time_sent': int(datetime.now().timestamp()) + 1,
        'is_pinned': False,
        'reacts':[
                {
                    'react_id': 1,
                    'u_ids': [], 
                    'is_this_user_reacted': False
                }
            ]
    })

    time.sleep(2) 

    r1 = requests.get(config.url + 'channel/messages/v2', params={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'start': 0,
    })
    payload = r1.json()
   
    assert len(payload['messages']) == 1
    assert resp.status_code == 200

def test_message_less_than_one_character_message_send_later():
    requests.delete(config.url + 'clear/v1')

    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()

    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_token['token'], 
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id = channel.json()

    resp = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'message': "",
        'time_sent': int(datetime.now().timestamp()) + 5,
        'is_pinned': False,
        'reacts':[
                {
                    'react_id': 1,
                    'u_ids': [], 
                    'is_this_user_reacted': False
                }
            ]
    })

    assert resp.status_code == InputError.code

def test_message_more_than_one_thousand_character_message_send_later():
    requests.delete(config.url + 'clear/v1')

    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()

    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_token['token'], 
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id = channel.json()
    
    resp = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'message': "f" * 1001,
        'time_sent': int(datetime.now().timestamp()) + 5,
        'is_pinned': False,
        'reacts':[
                {
                    'react_id': 1,
                    'u_ids': [], 
                    'is_this_user_reacted': False
                }
            ]
    })

    assert resp.status_code == InputError.code
