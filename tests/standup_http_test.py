import requests
from src import config
from src.error import InputError, AccessError

'''
Tests for standup/start
'''

def test_standup_start_invalid_channel_id():
    '''
    Case: channel_id does not refer to a valid channel
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    payload1 = r1.json()

    r2 = requests.post(config.url + 'standup/start/v1', json={
        'token': payload1['token'],
        'channel_id': -1,
        'length': 33,
    })

    assert r2.status_code == InputError.code

def test_standup_start_invalid_length():
    '''
    Case: length is a negative integer
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    payload1 = r1.json()

    r2 = requests.post(config.url + 'channels/create/v2', json={
        'token': payload1['token'],
        'name': 'Alpaca',
        'is_public': True,
    })
    payload2 = r2.json()

    r3 = requests.post(config.url + 'standup/start/v1', json={
        'token': payload1['token'],
        'channel_id': payload2['channel_id'],
        'length': -33,
    })

    assert r3.status_code == InputError.code

'''
def test_standup_start_already_active_standup():

    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    payload1 = r1.json()

    r2 = requests.post(config.url + 'channels/create/v2', json={
        'token': payload1['token'],
        'name': 'Alpaca',
        'is_public': True,
    })
    payload2 = r2.json()

    requests.post(config.url + 'standup/start/v1', json={
        'token': payload1['token'],
        'channel_id': payload2['channel_id'],
        'length': 33,
    })
    
    r3 = requests.post(config.url + 'standup/start/v1', json={
        'token': payload1['token'],
        'channel_id': payload2['channel_id'],
        'length': 66,
    })

    assert r3.status_code == InputError.code
'''

def test_standup_start_not_a_member():
    '''
    Case: channel_id is valid and the authorised user is not a member of the channel
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    payload1 = r1.json()

    r2 = requests.post(config.url + 'channels/create/v2', json={
        'token': payload1['token'],
        'name': 'Alpaca',
        'is_public': True,
    })
    payload2 = r2.json()

    r3 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user2@email.com',
        'password': 'user2password',
        'name_first': 'Kim',
        'name_last': 'Kardashian',
    })
    payload3 = r3.json()

    r4 = requests.post(config.url + 'standup/start/v1', json={
        'token': payload3['token'],
        'channel_id': payload2['channel_id'],
        'length': 33,
    })

    assert r4.status_code == AccessError.code



'''
Tests for standup/start
'''

def test_standup_active_invalid_channel():
    '''
    Case: channel_id does not refer to a valid channel
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    payload1 = r1.json()

    r2 = requests.get(config.url + 'standup/active/v1', params={
        'token': payload1['token'],
        'channel_id': -1,
    })

    assert r2.status_code == InputError.code
    
def test_standup_active_not_channel_member():
    '''
    Case: channel_id is valid and the authorised user is not a member of the channel
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    payload1 = r1.json()

    r2 = requests.post(config.url + 'channels/create/v2', json={
        'token': payload1['token'],
        'name': 'Alpaca',
        'is_public': True,
    })
    payload2 = r2.json()

    requests.post(config.url + 'standup/start/v1', json={
        'token': payload1['token'],
        'channel_id': payload2['channel_id'],
        'length': 33,
    })

    r3 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user2@email.com',
        'password': 'user2password',
        'name_first': 'Kim',
        'name_last': 'Kardashian',
    })
    payload3 = r3.json()

    r4 = requests.get(config.url + 'standup/active/v1', params={
        'token': payload3['token'],
        'channel_id': payload2['channel_id'],
    })

    assert r4.status_code == AccessError.code

def test_standup_active_invalid_token():
    '''
    Case: non registered user tried to call standup/active
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    payload1 = r1.json()

    r2 = requests.post(config.url + 'channels/create/v2', json={
        'token': payload1['token'],
        'name': 'Alpaca',
        'is_public': True,
    })
    payload2 = r2.json()

    r3 = requests.get(config.url + 'standup/active/v1', params={
        'token': 'invalidtoken',
        'channel_id': payload2['channel_id'],
    })

    assert r3.status_code == AccessError.code