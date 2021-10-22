import pytest
import requests
import json
from src import config
from src.other import clear_v1
import jwt

def test_invalid_dm_id_message_send_dm():
    '''
    Check if invalid dm_id is passed as input
    '''
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    user_reg = user.json()

    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_reg['token'],
        'u_ids': [],
    })
    dm_reg = dm.json()

    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_reg['token'], 
        'dm_id': dm_reg['dm_id'] + 1,
        'message': "hello",
    })
    assert resp.status_code == 400

def test_not_dm_member_message_send_dm():
    '''
    Check if invalid dm_id is passed as input
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    user2= requests.post(config.url + 'auth/register/v2', json={
        'email': 'user2@email.com',
        'password': 'user2password',
        'name_first': 'Kanye',
        'name_last': 'East',
    })

    user_reg1 = user1.json()
    user_reg2 = user2.json()

    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_reg1['token'],
        'u_ids': [],
    })
    dm_reg = dm.json()

    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_reg2['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
    })
    assert resp.status_code == 403

def test_invalid_token_message_send_dm():
    '''
    Check if invalid token is passed as input
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    payload1 = r1.json()

    r2 = requests.post(config.url + 'dm/create/v1', json={
        'token': payload1['token'],
        'u_ids': [],
    })
    payload2 = r2.json()

    r3 = requests.post(config.url + 'message/senddm/v1', json={
        'token': 'invalidtoken',
        'dm_id': payload2['dm_id'],
        'message': "hello"
    })
    assert r3.status_code == 403

def test_route_works_message_send_dm():
    requests.delete(config.url + 'clear/v1')

    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_reg = user.json()

    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_reg['token'], 
        'u_ids': [],
    })
    dm_reg = dm.json()

    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_reg['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
    })

    assert resp.status_code == 200

def test_message_less_than_one_character_message_send_dm():
    requests.delete(config.url + 'clear/v1')

    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_reg = user.json()

    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_reg['token'], 
        'u_ids': [],
    })
    dm_reg = dm.json()

    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_reg['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "",
    })

    assert resp.status_code == 400

def test_message_more_than_one_thousand_character_message_send_dm():
    requests.delete(config.url + 'clear/v1')

    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_reg = user.json()

    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_reg['token'], 
        'u_ids': [],
    })
    dm_reg = dm.json()

    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_reg['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "f" * 1001,
    })

    assert resp.status_code == 400

def test_check_messagge_ids_are_not_the_same_for_same_dm_id_message_send_dm():
    requests.delete(config.url + 'clear/v1')

    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_reg = user.json()

    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_reg['token'], 
        'u_ids': [],
    })
    dm_reg = dm.json()

    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_reg['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
    })
    
    resp2 = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_reg['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
    })
    message1 = resp.json()
    message2 = resp2.json()
    assert message1['message_id'] != message2['message_id']

def test_check_messagge_ids_are_not_the_same_for_different_dm_message_send_dm():
    requests.delete(config.url + 'clear/v1')

    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_reg = user.json()

    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_reg['token'], 
        'u_ids': [],
    })
    dm2 = requests.post(config.url + 'dm/create/v1', json={
        'token': user_reg['token'], 
        'u_ids': [],
    })
    dm_reg = dm.json()
    dm_reg2 = dm2.json()

    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_reg['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
    })
    
    resp2 = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_reg['token'], 
        'dm_id': dm_reg2['dm_id'],
        'message': "hello",
    })
    message1 = resp.json()
    message2 = resp2.json()
    assert message1['message_id'] != message2['message_id']

def test_check_messagge_ids_are_not_the_same_for_different_channel_and_dm_message_send():
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

    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_token['token'], 
        'u_ids': [],
    })
    dm_id = dm.json()
    
    resp = requests.post(config.url + 'message/send/v1', json={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'message': "hello",
    })
    resp2 = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_token['token'], 
        'dm_id': dm_id['dm_id'],
        'message': "hello",
    })

    message1 = resp.json()
    message2 = resp2.json()
    assert message1['message_id'] != message2['message_id']

