import pytest
import requests
import json
from src import config
from tests.pytest_fixtures import (
    clear, reg_user1, reg_user2, reg_dm_user1, send_dm_message_user1, send_2nd_dm_message_user1, 
    reg_dm_user2, send_dm_message_user2, reg_channel_user1, send_channel_message_user1
)
from src.error import InputError, AccessError


def test_invalid_dm_id_message_send_dm(clear, reg_user1, reg_dm_user1):
    user1 = reg_user1
    dm_reg = reg_dm_user1

    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'] + 1,
        'message': "hello",
    })
    assert resp.status_code == InputError.code

def test_not_dm_member_message_send_dm(clear, reg_user2, reg_dm_user1):
    user2 = reg_user2
    dm_reg = reg_dm_user1

    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user2['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
    })
    assert resp.status_code == AccessError.code

def test_invalid_token_message_send_dm(clear, reg_dm_user1):
    dm_reg = reg_dm_user1

    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': 'invalidtoken',
        'dm_id': dm_reg['dm_id'],
        'message': "hello"
    })
    assert resp.status_code == AccessError.code

def test_route_works_message_send_dm(clear, reg_user1, reg_dm_user1):
    user1 = reg_user1
    dm_reg = reg_dm_user1

    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
    })

    assert resp.status_code == 200

def test_message_less_than_one_character_message_send_dm(clear, reg_user1, reg_dm_user1):
    user1 = reg_user1
    dm_reg = reg_dm_user1

    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "",
    })

    assert resp.status_code == InputError.code

def test_message_more_than_one_thousand_character_message_send_dm(clear, reg_user1, reg_dm_user1):
    user1 = reg_user1
    dm_reg = reg_dm_user1

    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "f" * 1001,
    })

    assert resp.status_code == InputError.code

def test_check_messagge_ids_are_not_the_same_for_same_dm_id_message_send_dm(
    clear, send_dm_message_user1, send_2nd_dm_message_user1 
):
    message_id1 = send_dm_message_user1
    message_id2 = send_2nd_dm_message_user1
    
    assert message_id1 != message_id2

def test_check_messagge_ids_are_not_the_same_for_different_dm_message_send_dm(
    clear, send_dm_message_user1, send_dm_message_user2
):
    message_id1 = send_dm_message_user1
    message_id2 = send_dm_message_user2
    
    assert message_id1 != message_id2

def test_check_messagge_ids_are_not_the_same_for_different_channel_and_dm_message_send(
    clear, send_channel_message_user1, send_dm_message_user1
):
    message_id1 = send_channel_message_user1
    message_id2 = send_dm_message_user1
    
    assert message_id1 != message_id2

