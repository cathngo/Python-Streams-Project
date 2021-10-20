import pytest
import requests
import json
from src import config
from src.other import clear_v1
import jwt
from tests.dm_details_http_test import (
    test_not_dm_member,
    test_invalid_dm_id,
    test_invalid_token,
)

#tests that there is a negative one when the end of a message is reached
def test_negative_one_end_of_messages_dm():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_reg = user.json()
    #create a dm with that user
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_reg['token'], 
        'u_ids': [user_reg['auth_user_id']],
    })
    dm_reg = dm.json()
    #pass in a start that is greater to the number of messages in the system
    response = requests.get(config.url + 'dm/messages/v1', params={
        'token': user_reg['token'], 
        'dm_id': dm_reg['dm_id'],
        'start': 0,
    })
    #get the response in json
    do = response.json()
    assert do['end'] == -1


def test_start_greater_than_messages():
    requests.delete(config.url + 'clear/v1')
     #create a user
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_reg = user.json()
    #create a dm with that user
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_reg['token'], 
        'u_ids': [user_reg['auth_user_id']],
    })
    dm_reg = dm.json()
    #pass in a start that is greater to the number of messages in the system
    resp = requests.get(config.url + 'dm/messages/v1', params={
        'token': user_reg['token'], 
        'dm_id': dm_reg['dm_id'],
        'start': 1,
    })
    #get the response in json
    do = resp.json()
    print(do)
    assert resp.status_code == 400