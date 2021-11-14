import pytest
import requests
import json
from src import channel, config
import jwt
import random
import string
from src.error import InputError, AccessError
from tests.pytest_fixtures import (
    clear, reg_user1, reg_user2, reg_channel_user1, send_channel_message_user1, 
    send_channel_message_user2, send_dm_message_user1, reg_dm_user1, reg_dm_2users, 
    send_dm_message_user1_in_dm_with_two_users, user2_channel_join, send_channel_message_with_two_users_user2, 
    send_dm_message_user2_in_dm_with_two_users,reg_channel_user2
)

def test_search_invalid_token(
    clear, reg_user1, send_channel_message_user1
    ):
    user1 = reg_user1
    query = "hello"
    #create invalid token
    invalid_token = jwt.encode({'u_id': user1['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')

    #unreact to message with the invalid token
    r = requests.get(config.url + "search/v1", params={ 
        'token': invalid_token,
        'query_str': query
    })
    assert r.status_code == AccessError.code 

def test_search_invalid_query(clear, reg_user1):
    user1 = reg_user1
    query_over_1000 = ''.join((random.choice(string.ascii_lowercase) for x in range(1002)))
    r = requests.get(config.url + "search/v1", params={'token': user1['token'],'query_str': query_over_1000})
    assert r.status_code == InputError.code 

#create 2 channels, where user1 only belongs to one 
def test_search_channels(
    clear, reg_user1, reg_user2, reg_channel_user1, send_channel_message_user2,send_channel_message_with_two_users_user2, send_channel_message_user1, 
    ):
    user1 = reg_user1
    user2 = reg_user2
    channel1 = reg_channel_user1
    #Send message that does not contain the given query
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'], 'channel_id': channel1,'message': "does not contain the query",})
    resp = requests.get(config.url + "search/v1", params={'token': user1['token'],'query_str': 'hello'})
    mess = resp.json()
    assert len(mess['messages']) == 2

def test_search_dms(
    clear, reg_user1, reg_user2, reg_dm_user1, send_dm_message_user1
    ):
    user1 = reg_user1
    dm_reg = reg_dm_user1
    requests.post(config.url + 'message/senddm/v1', json={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "message2",
    })
    query = "message2"
    resp = requests.get(config.url + "search/v1", params={'token': user1['token'],'query_str': query})
    mess = resp.json()
    assert len(mess['messages']) == 1

def test_search_not_in_dm(
    clear, reg_user1, reg_user2, reg_dm_user1
    ):
    user2 = reg_user2
    query = "hello"
    resp = requests.get(config.url + "search/v1", params={'token': user2['token'],'query_str': query})
    mess = resp.json()
    assert len(mess['messages']) == 0