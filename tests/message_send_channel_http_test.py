import pytest
import requests
import json
from src import config
import jwt
from src.error import InputError, AccessError
from tests.pytest_fixtures import (
    clear, reg_user1, reg_user2, reg_channel_user1, send_channel_message_user1, 
    send_2nd_channel_message_user1, reg_channel_user2, send_channel_message_user2, 
    send_dm_message_user1, reg_dm_user1
)

def test_invalid_channel_id_message_send(clear, reg_user1):
    invalid_channel_id = 1000
    user1 = reg_user1
    
    resp = requests.post(config.url + 'message/send/v1', json={
        'token': user1['token'],
        'channel_id': invalid_channel_id,
        'message': "hello"
    })
    assert resp.status_code == InputError.code

def test_unauthorised_user_message_send(clear, reg_channel_user1, reg_user2):
    channel_id = reg_channel_user1
    unauthorised_user = reg_user2

    resp = requests.post(config.url + 'message/send/v1', json={
        'token': unauthorised_user['token'], 
        'channel_id': channel_id,
        'message': "hello"
    })
    assert resp.status_code == AccessError.code

def test_invalid_token_signature_message_send(clear, reg_channel_user1, reg_user1):
    channel_id = reg_channel_user1
    user1 = reg_user1
    #create invalid token
    invalid_token = jwt.encode({'u_id': user1['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')
    #pass valid channel id but invalid token
    resp = requests.post(config.url + 'message/send/v1', json={
        'token': invalid_token, 
        'channel_id': channel_id,
        'message': "hello"
    })
    assert resp.status_code == AccessError.code

def test_route_works_message_send(clear, reg_channel_user1, reg_user1, send_channel_message_user1):
    channel_id = reg_channel_user1
    user1 = reg_user1

    resp = requests.post(config.url + 'message/send/v1', json={
        'token': user1['token'], 
        'channel_id': channel_id,
        'message': "hello",
    })

    assert resp.status_code == 200

def test_message_less_than_one_character_message_send(clear, reg_channel_user1, reg_user1):
    channel_id = reg_channel_user1
    user1 = reg_user1

    resp = requests.post(config.url + 'message/send/v1', json={
        'token': user1['token'], 
        'channel_id': channel_id,
        'message': ""
    })

    assert resp.status_code ==  InputError.code

def test_message_more_than_one_thousand_character_message_send(clear, reg_channel_user1, reg_user1):
    user1 = reg_user1
    channel_id = reg_channel_user1
    
    resp = requests.post(config.url + 'message/send/v1', json={
        'token': user1['token'], 
        'channel_id': channel_id,
        'message': "f" * 1001
    })
    assert resp.status_code == InputError.code

def test_check_message_ids_are_not_the_same_for_same_channel_message_send (
    clear, reg_channel_user1, send_channel_message_user1, send_2nd_channel_message_user1
):
    message_id1 = send_channel_message_user1
    message_id2 = send_2nd_channel_message_user1

    assert message_id1 != message_id2

def test_check_messagge_ids_are_not_the_same_for_different_channel_message_send(
    clear, send_channel_message_user1, send_channel_message_user2
):
    message_id1 = send_channel_message_user1
    message_id2 = send_channel_message_user2

    assert message_id1 != message_id2

def test_check_messagge_ids_are_not_the_same_for_different_channel_and_dm_message_send(
    clear, send_channel_message_user1, send_dm_message_user1
):
    message_id1 = send_channel_message_user1
    message_id2 = send_dm_message_user1
    
    assert message_id1 != message_id2

