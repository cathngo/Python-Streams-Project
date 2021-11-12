import pytest
import time
from datetime import datetime
import requests
import json
from src import config
from tests.pytest_fixtures import (
    clear, reg_user1, reg_user2, reg_dm_user1, send_dm_message_user1, send_2nd_dm_message_user1, 
    reg_dm_user2, send_dm_message_user2, reg_channel_user1, send_channel_message_user1
)
from src.error import InputError, AccessError

def test_invalid_token_dm_messages_later(clear, reg_dm_user1):
    dm_reg = reg_dm_user1

    resp = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': 'invalidtoken',
        'dm_id': dm_reg['dm_id'] + 1,
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

def test_invalid_dm_id_message_send_dm_later(clear, reg_user1, reg_dm_user1):
    user1 = reg_user1
    dm_reg = reg_dm_user1

    resp = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user1['token'],
        'dm_id': dm_reg['dm_id'] + 1,
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

def test_not_dm_member_message_send_dm_later(clear, reg_user2, reg_dm_user1):
    user2 = reg_user2
    dm_reg = reg_dm_user1

    resp = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user2['token'], 
        'dm_id': dm_reg['dm_id'],
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


def test_route_works_message_send_dm_later(clear, reg_user1, reg_dm_user1):
    user1 = reg_user1
    dm_reg = reg_dm_user1

    resp = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'],
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

    response = requests.get(config.url + 'dm/messages/v1', params={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'],
        'start': 0,
    })
    dm_messages = response.json()

    assert len(dm_messages['messages']) == 1
    assert resp.status_code == 200

def test_message_less_than_one_character_message_send_dm_later(clear, reg_user1, reg_dm_user1):
    user1 = reg_user1
    dm_reg = reg_dm_user1

    resp = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'],
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

def test_message_more_than_one_thousand_character_message_send_dm_later(clear, reg_user1, reg_dm_user1):
    user1 = reg_user1
    dm_reg = reg_dm_user1

    resp = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'],
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