import requests
from src import config
from src.error import InputError, AccessError

'''
Tests for message/share
'''

def test_both_invalid_id():
    '''
    Case: both channel_id and dm_id are invalid
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

    r3 = requests.post(config.url + 'message/send/v1', json={
        'token': payload1['token'], 
        'channel_id': payload2['channel_id'],
        'message': "Hello",
    })
    payload3 = r3.json()

    r4 = requests.post(config.url + 'message/share/v1', json={
        'token': payload1['token'],
        'og_message_id': payload3['message_id'],
        'message': 'Hello Again',
        'channel_id': -100,
        'dm_id': -100,
    })

    assert r4.status_code == InputError.code

def test_both_valid_ids():
    '''
    Case: neither channel_id nor dm_id are -1
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

    r3 = requests.post(config.url + 'message/send/v1', json={
        'token': payload1['token'], 
        'channel_id': payload2['channel_id'],
        'message': "Hello",
    })
    payload3 = r3.json()

    r4 = requests.post(config.url + 'channels/create/v2', json={
        'token': payload1['token'],
        'name': 'Tyson',
        'is_public': True,
    })
    payload4 = r4.json()

    r5 = requests.post(config.url + 'dm/create/v1', json={
        'token': payload1['token'],
        'u_ids': [],
    })
    payload5 = r5.json()

    r6 = requests.post(config.url + 'message/share/v1', json={
        'token': payload1['token'],
        'og_message_id': payload3['message_id'],
        'message': 'Hello Again',
        'channel_id': payload4['channel_id'],
        'dm_id': payload5['dm_id'],
    })

    assert r6.status_code == InputError.code

def test_invalid_og_message_id():
    '''
    Case: og_message_id does not refer to a valid message within a
    channel/DM that the authorised user has joined
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

    requests.post(config.url + 'dm/create/v1', json={
        'token': payload1['token'],
        'u_ids': [],
    })

    r3 = requests.post(config.url + 'message/share/v1', json={
        'token': payload1['token'],
        'og_message_id': -1,
        'message': 'Hello Again',
        'channel_id': payload2['channel_id'],
        'dm_id': -1,
    })

    assert r3.status_code == InputError.code

def test_invalid_message_length():
    '''
    Case: length of message is more than 1000 characters
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

    r3 = requests.post(config.url + 'message/send/v1', json={
        'token': payload1['token'], 
        'channel_id': payload2['channel_id'],
        'message': "Hello",
    })
    payload3 = r3.json()

    r4 = requests.post(config.url + 'dm/create/v1', json={
        'token': payload1['token'],
        'u_ids': [],
    })
    payload4 = r4.json()

    r5 = requests.post(config.url + 'message/share/v1', json={
        'token': payload1['token'],
        'og_message_id': payload3['message_id'],
        'message': 'Messagelengthistoolong' * 100,
        'channel_id': -1,
        'dm_id': payload4['dm_id'],
    })

    assert r5.status_code == InputError.code

def test_non_member_shares():
    '''
    Case: the pair of channel_id and dm_id are valid (i.e. one is -1, the other is valid)
    and the authorised user has not joined the channel or DM they are trying to share the message to
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

    r3 = requests.post(config.url + 'message/send/v1', json={
        'token': payload1['token'], 
        'channel_id': payload2['channel_id'],
        'message': "Hello",
    })
    payload3 = r3.json()

    r4 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user2@email.com',
        'password': 'user2password',
        'name_first': 'Tyson',
        'name_last': 'Fury',
    })
    payload4 = r4.json()

    r5 = requests.post(config.url + 'dm/create/v1', json={
        'token': payload4['token'],
        'u_ids': [],
    })
    payload5 = r5.json()

    r6 = requests.post(config.url + 'message/share/v1', json={
        'token': payload1['token'],
        'og_message_id': payload3['message_id'],
        'message': 'Hello Again',
        'channel_id': -1,
        'dm_id': payload5['dm_id'],
    })

    assert r6.status_code == AccessError.code

def test_invalid_token_member_shares():
    '''
    Case: non registered user tried to share a message into a valid dm
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

    r3 = requests.post(config.url + 'message/send/v1', json={
        'token': payload1['token'], 
        'channel_id': payload2['channel_id'],
        'message': "Hello",
    })
    payload3 = r3.json()

    r4 = requests.post(config.url + 'dm/create/v1', json={
        'token': payload1['token'],
        'u_ids': [],
    })
    payload4 = r4.json()

    r5 = requests.post(config.url + 'message/share/v1', json={
        'token': 'invalidtoken',
        'og_message_id': payload3['message_id'],
        'message': 'Hello Again',
        'channel_id': -1,
        'dm_id': payload4['dm_id'],
    })

    assert r5.status_code == AccessError.code

def test_message_share_works():
    '''
    Case: user is able to successfully share a messsage
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

    r3 = requests.post(config.url + 'message/send/v1', json={
        'token': payload1['token'], 
        'channel_id': payload2['channel_id'],
        'message': "Hello from Channel",
    })
    payload3 = r3.json()

    requests.post(config.url + 'dm/create/v1', json={
        'token': payload1['token'],
        'u_ids': [],
    })

    r4 = requests.post(config.url + 'dm/create/v1', json={
        'token': payload1['token'],
        'u_ids': [],
    })
    payload4 = r4.json()

    r5 = requests.post(config.url + 'message/senddm/v1', json={
        'token': payload1['token'], 
        'dm_id': payload4['dm_id'],
        'message': "Hello from DM",
    })
    payload5 = r5.json()

    requests.post(config.url + 'message/share/v1', json={
        'token': payload1['token'],
        'og_message_id': payload3['message_id'],
        'message': 'Works',
        'channel_id': -1,
        'dm_id': payload4['dm_id'],
    })
    requests.post(config.url + 'message/share/v1', json={
        'token': payload1['token'],
        'og_message_id': payload5['message_id'],
        'message': 'Works',
        'channel_id': payload2['channel_id'],
        'dm_id': -1,
    })

    r6 = requests.get(config.url + 'channel/messages/v2', params={
        'token': payload1['token'], 
        'channel_id': payload2['channel_id'],
        'start': 0
    })
    channel_res = r6.json()

    r7 = requests.get(config.url + 'dm/messages/v1', params={
        'token': payload1['token'], 
        'dm_id': payload4['dm_id'],
        'start': 0,
    })
    dm_res = r7.json()

    assert len(channel_res['messages']) == 2
    assert len(dm_res['messages']) == 2