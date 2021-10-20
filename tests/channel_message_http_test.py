import pytest
import requests
import json
from src import config
from src.other import clear_v1
import jwt
from tests.http_channel_details_v2_test import (
    test_invalid_channel_id,
    test_unauthorised_user,
    test_invalid_existing_channel_id,
    test_invalid_token_signature
)

test_invalid_channel_id()
test_unauthorised_user()
test_invalid_existing_channel_id()
test_invalid_token_signature()

#tests that there is a negative one when the end of a message is reached
def test_negative_one_end_of_messages():
    requests.delete(config.url + 'clear/v1')
     #create a user
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_token['token'], 
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id = channel.json()
    #pass in start when there are no more messages
    resp = requests.get(config.url + 'channel/message/v2', params={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'start': 0,
    })
    #get the response in json
    messages = resp.json()
    assert messages['end'] == -1


def test_start_greater_than_messages():
    requests.delete(config.url + 'clear/v1')
     #create a user
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_token['token'], 
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id = channel.json()
    #pass in a start that is greater to the number of messages in the system
    resp = requests.get(config.url + 'channel/message/v2', params={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'start': 1,
    })
    #get the response in json
    assert resp.status_code == 400

