import pytest
import requests
import json
from src import config
from src.other import clear_v1
import jwt
from src.error import InputError, AccessError
from tests.pytest_fixtures import clear, reg_user1, reg_user2, reg_channel_user1

def test_invalid_channel_id_channel_messages(clear, reg_user1):
    user1 = reg_user1
    invalid_channel_id = 1000
    
    resp = requests.get(config.url + 'channel/messages/v2', params={
        'token': user1['token'],
        'channel_id': invalid_channel_id,
        'start': 0
    })
    assert resp.status_code == InputError.code

def test_unauthorised_user_channel_messages(clear, reg_user2, reg_channel_user1):
    channel_id = reg_channel_user1
    
    user_not_in_channel = reg_user2
    
    resp = requests.get(config.url + 'channel/messages/v2', params={
        'token': user_not_in_channel['token'], 
        'channel_id': channel_id,
        'start': 0
    })
    assert resp.status_code == AccessError.code

def test_invalid_token_signature_channel_messages(clear, reg_user1, reg_channel_user1):
    #create user
    user1 = reg_user1
    #create channel with that user
    channel_id = reg_channel_user1
    #create invalid token
    invalid_token = jwt.encode({'u_id': user1['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')
    #pass valid channel id but invalid token
    resp = requests.get(config.url + 'channel/messages/v2', params={
        'token': invalid_token, 
        'channel_id': channel_id,
        'start': 0
    })
    assert resp.status_code == AccessError.code

def test_channel_messages_route_works(clear, reg_user1, reg_channel_user1):
    #create a user
    user1 = reg_user1
    #create a channel with that user
    channel_id = reg_channel_user1
    #pass in a start that is greater to the number of messages in the system
    resp = requests.get(config.url + 'channel/messages/v2', params={
        'token': user1['token'], 
        'channel_id': channel_id,
        'start': 0,
    })
    #get the response in json
    assert resp.status_code == 200

#tests that there is a negative one when the end of a message is reached
def test_negative_one_end_of_messages_channel_messages(clear, reg_user1, reg_channel_user1):
    #create a user
    user1 = reg_user1
    #create a channel with that user
    channel_id = reg_channel_user1
    #pass in start when there are no more messages
    resp = requests.get(config.url + 'channel/messages/v2', params={
        'token': user1['token'], 
        'channel_id': channel_id,
        'start': 0,
    })
    #get the response in json
    messages = resp.json()
    assert messages['end'] == -1


def test_start_greater_than_messages_channel_messages(clear, reg_user1, reg_channel_user1):
    #create a user
    user1 = reg_user1
    #create a channel with that user
    channel_id = reg_channel_user1
    #pass in start when there are no more messages
    resp = requests.get(config.url + 'channel/messages/v2', params={
        'token': user1['token'], 
        'channel_id': channel_id,
        'start': 1,
    })
    #get the response in json
    assert resp.status_code == InputError.code

# Check pagination works when there are more than 50 messages
def test_pagination_works(clear, reg_user1, reg_channel_user1):
    #create a user
    user1 = reg_user1
    #create a channel with that user
    channel_id = reg_channel_user1

    for _ in range(60):
        requests.post(config.url + 'message/send/v1', json={
            'token': user1['token'], 
            'channel_id': channel_id,
            'message': "Repeat",
        })

    resp1 = requests.get(config.url + 'channel/messages/v2', params={
        'token': user1['token'], 
        'channel_id': channel_id,
        'start': 55,
    })
    resp2 = requests.get(config.url + 'channel/messages/v2', params={
        'token': user1['token'], 
        'channel_id': channel_id,
        'start': 0,
    })

    assert resp1.status_code == 200
    assert resp2.status_code == 200