import pytest
import requests
import json
from datetime import datetime
from src import config
from src.other import clear_v1
import jwt
from tests.message_send_dm_http_test import (
    test_check_messagge_ids_are_not_the_same_for_different_channel_and_dm_message_send
)

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
        'time_sent': int(datetime.now().timestamp()) + 5
    })
    assert resp.status_code == 400

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
    })
    assert resp.status_code == 403

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
        'time_sent': int(datetime.now().timestamp()) + 5 
    })
    assert resp.status_code == 403

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
        'time_sent': int(datetime.now().timestamp()) + 5,
    })

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
        'time_sent': int(datetime.now().timestamp()) + 5
    })

    assert resp.status_code == 400

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
        'time_sent': int(datetime.now().timestamp()) + 5
    })

    assert resp.status_code == 400
