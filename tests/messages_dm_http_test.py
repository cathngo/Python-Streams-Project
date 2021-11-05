import pytest
import requests
import json
from src import config
from src.error import InputError, AccessError
from tests.pytest_fixtures import clear, reg_user1, reg_user2, reg_dm_user1

def test_not_dm_member_dm_messages(clear, reg_user2, reg_dm_user1):
    user2 = reg_user2
    dm_reg = reg_dm_user1
    
    resp = requests.get(config.url + 'dm/messages/v1', params={
        'token': user2['token'], 
        'dm_id': dm_reg['dm_id'],
        'start': 0,
    })
    
    assert resp.status_code == AccessError.code

def test_invalid_dm_id_dm_messages(clear, reg_user1, reg_dm_user1):
    user1 = reg_user1
    dm_reg = reg_dm_user1

    resp = requests.get(config.url + 'dm/messages/v1', params={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'] + 1,
        'start': 0,
    })
    assert resp.status_code == InputError.code

def test_invalid_token_dm_messages(clear, reg_dm_user1):
    dm_reg = reg_dm_user1

    resp = requests.get(config.url + 'dm/messages/v1', params={
        'token': 'invalidtoken',
        'dm_id': dm_reg['dm_id'],
        'start': 0
    })
    assert resp.status_code == AccessError.code

def test_dm_messages_route_works(clear, reg_user1, reg_dm_user1):
    user1 = reg_user1
    dm_reg = reg_dm_user1
    
    resp = requests.get(config.url + 'dm/messages/v1', params={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'],
        'start': 0,
    })

    assert resp.status_code == 200

#tests that there is a negative one when the end of a message is reached
def test_negative_one_end_of_messages_dm(clear, reg_user1, reg_dm_user1):
    
    user1 = reg_user1
    dm_reg = reg_dm_user1

    response = requests.get(config.url + 'dm/messages/v1', params={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'],
        'start': 0,
    })

    dm_messages = response.json()
    assert dm_messages['end'] == -1


def test_start_greater_than_messages_dm(clear, reg_user1, reg_dm_user1):
    user1 = reg_user1
    dm_reg = reg_dm_user1

    resp = requests.get(config.url + 'dm/messages/v1', params={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'],
        'start': 1,
    })

    assert resp.status_code == InputError.code

# Check pagination works when there are more than 50 messages
def test_pagination_works(clear, reg_user1, reg_dm_user1):
    user1 = reg_user1
    dm_reg = reg_dm_user1

    for _ in range(60):
        requests.post(config.url + 'message/senddm/v1', json={
                'token': user1['token'], 
                'dm_id': dm_reg['dm_id'],
                'message': "repeat",
        })

    #pass in a start that is greater to the number of messages in the system
    resp1 = requests.get(config.url + 'dm/messages/v1', params={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'],
        'start': 55,
    })
    resp2 = requests.get(config.url + 'dm/messages/v1', params={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'],
        'start': 0,
    })

    assert resp1.status_code == 200
    assert resp2.status_code == 200