import requests
from src import config
from src.error import InputError, AccessError

'''
Tests for standup/start
'''

def test_invalid_channel_id():
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

def test_invalid_length():
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

def test_already_active_standup():
    '''
    Case: an active standup is currently running in the channel
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
    
    r3 = requests.post(config.url + 'standup/start/v1', json={
        'token': payload1['token'],
        'channel_id': payload2['channel_id'],
        'length': 66,
    })

    assert r3.status_code == InputError.code

def test_not_a_member():
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
        'email': 'user1@email.com',
        'password': 'user1password',
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