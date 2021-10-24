import pytest
import requests
import json
from src import config
from src.other import clear_v1
import jwt

def test_not_dm_member_dm_messages():
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

    resp = requests.get(config.url + 'dm/messages/v1', params={
        'token': user_reg2['token'], 
        'dm_id': dm_reg['dm_id'],
        'start': 0,
    })
    assert resp.status_code == 403

def test_invalid_dm_id_dm_messages():
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

    resp = requests.get(config.url + 'dm/messages/v1', params={
        'token': user_reg['token'], 
        'dm_id': dm_reg['dm_id'] + 1,
        'start': 0,
    })
    assert resp.status_code == 400

def test_invalid_token_dm_messages():
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

    r3 = requests.get(config.url + 'dm/messages/v1', params={
        'token': 'invalidtoken',
        'dm_id': payload2['dm_id'],
        'start': 0
    })
    assert r3.status_code == 403

def test_dm_messages_route_works():
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
    resp = requests.get(config.url + 'dm/messages/v1', params={
        'token': user_reg['token'], 
        'dm_id': dm_reg['dm_id'],
        'start': 0,
    })

    assert resp.status_code == 200

#tests that there is a negative one when the end of a message is reached
def test_negative_one_end_of_messages_dm():
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

    response = requests.get(config.url + 'dm/messages/v1', params={
        'token': user_reg['token'], 
        'dm_id': dm_reg['dm_id'],
        'start': 0,
    })

    dm_messages = response.json()
    assert dm_messages['end'] == -1


def test_start_greater_than_messages_dm():
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
    
    #pass in a start that is greater to the number of messages in the system
    resp = requests.get(config.url + 'dm/messages/v1', params={
        'token': user_reg['token'], 
        'dm_id': dm_reg['dm_id'],
        'start': 1,
    })

    assert resp.status_code == 400

# Check pagination works when there are more than 50 messages
def test_pagination_works():
    requests.delete(config.url + 'clear/v1')

    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()

    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_token['token'], 
        'u_ids': [],
    })
    dm_reg = dm.json()

    for _ in range(60):
        requests.post(config.url + 'message/senddm/v1', json={
                'token': user_token['token'], 
                'dm_id': dm_reg['dm_id'],
                'message': "repeat",
        })

    #pass in a start that is greater to the number of messages in the system
    resp1 = requests.get(config.url + 'dm/messages/v1', params={
        'token': user_token['token'], 
        'dm_id': dm_reg['dm_id'],
        'start': 55,
    })
    resp2 = requests.get(config.url + 'dm/messages/v1', params={
        'token': user_token['token'], 
        'dm_id': dm_reg['dm_id'],
        'start': 55,
    })

    assert resp1.status_code == 200
    assert resp2.status_code == 200