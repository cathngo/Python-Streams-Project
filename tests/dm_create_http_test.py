import requests
from src import config

def test_dm_create_works():
    '''
    Check if dm/create/v1 returns expected output
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    r2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user2@email.com',
        'password': 'user2password',
        'name_first': 'Kanye',
        'name_last': 'East',
    })
    payload1 = r1.json()
    payload2 = r2.json()

    r3 = requests.post(config.url + 'dm/create/v1', json={
        'token': payload1['token'],
        'u_ids': [payload2['auth_user_id']],
    })
    payload3 = r3.json()
    assert len(payload3) == 1

def test_invalid_token():
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
        'token': 'invalidtoken',
        'u_ids': [payload1['auth_user_id']],
    })
    assert r2.status_code == 403

def test_empty_u_ids():
    '''
    Check that user can create dm with 0 members
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
    assert len(payload2) == 1

def test_invalid_u_ids():
    '''
    Check when any u_id in u_ids does not refer to a valid user
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    r2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user2@email.com',
        'password': 'user2password',
        'name_first': 'Kanye',
        'name_last': 'East',
    })
    payload1 = r1.json()
    payload2 = r2.json()

    r2 = requests.post(config.url + 'dm/create/v1', json={
        'token': payload1['token'],
        'u_ids': [payload2['auth_user_id'] + 1],
    })
    assert r2.status_code == 400

def test_unique_dm_id():
    '''
    Check if dm's are assigned unique ids
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    r2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user2@email.com',
        'password': 'user2password',
        'name_first': 'Kanye',
        'name_last': 'East',
    })
    payload1 = r1.json()
    payload2 = r2.json()

    r3 = requests.post(config.url + 'dm/create/v1', json={
        'token': payload1['token'],
        'u_ids': [payload2['auth_user_id']],
    })
    r4 = requests.post(config.url + 'dm/create/v1', json={
        'token': payload2['token'],
        'u_ids': [payload1['auth_user_id']],
    })
    payload3 = r3.json()
    payload4 = r4.json()
    assert payload3['dm_id'] != payload4['dm_id']