import requests
from src import config

def test_dm_list_works():
    '''
    Check if dm/list/v1 returns expected output
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

    requests.post(config.url + 'dm/create/v1', json={
        'token': payload1['token'],
        'u_ids': [payload2['auth_user_id']],
    })
    requests.post(config.url + 'dm/create/v1', json={
        'token': payload1['token'],
        'u_ids': [],
    })
    
    r3 = requests.get(config.url + 'dm/list/v1', params={
        'token': payload1['token'],
    })
    assert r3.status_code == 200

def test_no_dms():
    '''
    Check when user has 0 dms
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    payload1 = r1.json()

    r2 = requests.get(config.url + 'dm/list/v1', params={
        'token': payload1['token'],
    })
    payload2 = r2.json()
    assert len(payload2['dms']) == 0

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

    requests.post(config.url + 'dm/create/v1', json={
        'token': payload1['token'],
        'u_ids': [],
    })

    r2 = requests.get(config.url + 'dm/list/v1', params={
        'token': 'invalidtoken',
    })
    assert r2.status_code == 403