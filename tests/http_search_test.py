from email import message
import pytest
import requests
import json
from src import config
import jwt
from src.error import InputError, AccessError
from tests.pytest_fixtures import (
    clear, reg_user1, reg_user2, reg_channel_user1, send_channel_message_user1, 
    send_channel_message_user2, send_dm_message_user1, reg_dm_user1, reg_dm_2users, 
    send_dm_message_user1_in_dm_with_two_users, user2_channel_join, send_channel_message_with_two_users_user2, 
    send_dm_message_user2_in_dm_with_two_users
)

def test_search_invalid_token(
    clear, reg_user1, send_channel_message_user1, user1_react_to_their_message_in_channel
    ):
    user1 = reg_user1
    query = "hello"
    #create invalid token
    invalid_token = jwt.encode({'u_id': user1['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')

    #unreact to message with the invalid token
    r = requests.get(config.url + "/search/v1", params={ 
        'token': invalid_token,
        'query_str': query
    })
    assert r.status_code == AccessError.code 

def test_search_channels(
    clear, reg_user1, reg_user2, reg_channel_user1, send_channel_message_user1, 
    ):
    user1 = reg_user1
    query = "hello"

    r = requests.get(config.url + "/search/v1", params={ 
        'token': user1['token'],
        'query_str': query
    })
    messages = r.json()['messages']

    assert len(messages) == 1 

