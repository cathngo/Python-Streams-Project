import pytest
import requests
import json
from src import config
import jwt
import time
from datetime import datetime

#check stats are 0 when user first registers
def test_initalise_stats():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #get token from auth reg
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    resp = requests.get(config.url + 'user/stats/v1', params={'token': user_token['token']})
    r = resp.json()
    assert r['user_stats']['channels_joined'][0]['num_channels_joined'] == 0
    assert r['user_stats']['dms_joined'][0]['num_dms_joined'] == 0
    assert r['user_stats']['messages_sent'][0]['num_messages_sent'] == 0

#test involvement_rate is 0 when denom is 0
def test_involvement_rate_zero():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #get token from auth reg
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    resp = requests.get(config.url + 'user/stats/v1', params={'token': user_token['token']})
    r = resp.json()
    assert r['user_stats']['involvement_rate'] == float(0)

#check involvment_rate is 1 when involvment > 1 (when more msgs sent than msgs in database)
def test_involvement_rate_one():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #Register two users
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'valid1email@gmail.com', 'password': '123abc!@#', 'name_first': 'Becky', 'name_last': 'Smile'})
    user1_token = user1.json()
    user2_token = user2.json()
    #create a dm
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user1_token['token'],
        'u_ids': [user2_token['auth_user_id']],
    })
    dm_reg = dm.json()
    #send two msgs
    msg1 = requests.post(config.url + 'message/senddm/v1', json={
        'token': user1_token['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
    })
    msg2 = requests.post(config.url + 'message/senddm/v1', json={
        'token': user1_token['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "helloagain",
    })
    msg1_id = msg1.json()
    msg2_id = msg2.json()
    #remove two msgs
    requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user1_token['token'],
        'message_id': msg1_id['message_id'], 
    })  
    requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user1_token['token'],
        'message_id': msg2_id['message_id'], 
    })  
    #get user stats
    resp = requests.get(config.url + 'user/stats/v1', params={'token': user1_token['token']})
    r = resp.json()
    #involvement rate should be 3(num_dms_joined is one, num_messages_sent is 2) / 1 (num_dms_exist is one, num_messages_exist 0)
    assert r['user_stats']['involvement_rate'] == float(1)

#check correct involvement rate for < 0 and > 1
def test_involvement_rate_between_zero_one():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #Register two users
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'valid1email@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user1_token = user1.json()
    user2_token = user2.json()
    #create two channels for first user
    channel1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_token['token'], 'name': 'Alpaca', 'is_public': True})
    requests.post(config.url + 'channels/create/v2', json={'token': user1_token['token'], 'name': 'Snow', 'is_public': True})
    channel1_id = channel1.json() 
    #get user2 to join one of the channels
    requests.post(config.url + 'channel/join/v2', json={'token': user2_token['token'], 'channel_id': channel1_id['channel_id']})
    #get user stats
    resp = requests.get(config.url + 'user/stats/v1', params={'token': user2_token['token']})
    r = resp.json()
    resp2 = requests.get(config.url + 'user/stats/v1', params={'token': user1_token['token']})
    r2 = resp2.json()
    assert r2['user_stats']['involvement_rate'] == float(1)
    #involvement rate should be 1/2
    assert r['user_stats']['involvement_rate'] == float(1/2)

#check correct channels_joined
def test_correct_channels_joined():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #get token from auth reg
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create two
    channel1 = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel2 = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Snow', 'is_public': True})
    channel1_id = channel1.json() 
    channel2_id = channel2.json()
    #join two channels
    requests.post(config.url + 'channel/join/v2', json={'token': user_token['token'], 'channel_id': channel1_id['channel_id']})
    requests.post(config.url + 'channel/join/v2', json={'token': user_token['token'], 'channel_id': channel2_id['channel_id']})
    #leave one channel
    requests.post(config.url + 'channel/leave/v1', json={'token': user_token['token'], 'channel_id': channel1_id['channel_id']})
    #get user stats
    resp = requests.get(config.url + 'user/stats/v1', params={'token': user_token['token']})
    r = resp.json()
    #user joined two then left one channel, so num_channels_joined is 1
    assert r['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1

#check correct dms_joined
def test_correct_dms_joined():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #Register threeusers
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'valid1email@gmail.com', 'password': '123abc!@#', 'name_first': 'Becky', 'name_last': 'Smile'})
    user3 = requests.post(config.url + 'auth/register/v2', json={'email': 'valid2email@gmail.com', 'password': '123abc!@#', 'name_first': 'George', 'name_last': 'Peach'})
    user1_token = user1.json()
    user2_token = user2.json()
    user3_token = user3.json()
    #create two dms
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user1_token['token'],
        'u_ids': [user2_token['auth_user_id']],
    })
    dm_reg = dm.json()
    requests.post(config.url + 'dm/create/v1', json={
        'token': user1_token['token'],
        'u_ids': [user3_token['auth_user_id']],
    })
    #leave one dm
    requests.post(config.url + 'dm/leave/v1', json={
        'token': user1_token['token'],
        'dm_id': dm_reg['dm_id'],
    })
    #get user stats
    resp = requests.get(config.url + 'user/stats/v1', params={'token': user1_token['token']})
    r = resp.json()
    #num dms joined should be 1 (joined 2, left one = 1)
    assert r['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1

#check correct messages_sent
def test_correct_messages_sent_dm():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #Register threeusers
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'valid1email@gmail.com', 'password': '123abc!@#', 'name_first': 'Becky', 'name_last': 'Smile'})
    user1_token = user1.json()
    user2_token = user2.json()
    #create a dms
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user1_token['token'],
        'u_ids': [user2_token['auth_user_id']],
    })
    dm_reg = dm.json()
    #send two messages
    #send two msgs
    msg1 = requests.post(config.url + 'message/senddm/v1', json={
        'token': user1_token['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
    })
    requests.post(config.url + 'message/senddm/v1', json={
        'token': user1_token['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "helloagain",
    })
    msg1_id = msg1.json()
    #remove one message
    requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user1_token['token'],
        'message_id': msg1_id['message_id'], 
    })  
    #get user stats
    resp = requests.get(config.url + 'user/stats/v1', params={'token': user1_token['token']})
    r = resp.json()
    #sent two msgs, removed a msg but total sent msgs should still be two
    assert r['user_stats']['messages_sent'][-1]['num_messages_sent'] == 2

#check correct messages_sent
def test_correct_messages_sent_channel():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #Register a user
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user1_token = user1.json()
    #create a channel
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user1_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel_id = channel.json() 
    #send two messages
    msg1 = requests.post(config.url + 'message/send/v1', json={
        'token': user1_token['token'], 
        'channel_id': channel_id['channel_id'],
        'message': "hello",
    })
    msg1 = requests.post(config.url + 'message/send/v1', json={
        'token': user1_token['token'], 
        'channel_id': channel_id['channel_id'],
        'message': "helloo",
    })
    msg1_id = msg1.json()
    #remove one message
    requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user1_token['token'],
        'message_id': msg1_id['message_id'], 
    })  
    #get user stats
    resp = requests.get(config.url + 'user/stats/v1', params={'token': user1_token['token']})
    r = resp.json()
    #sent two msgs, removed a msg but total sent msgs should still be two
    assert r['user_stats']['messages_sent'][-1]['num_messages_sent'] == 2


def test_message_share():
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
    #get user stats
    resp = requests.get(config.url + 'user/stats/v1', params={'token': payload1['token']})
    r = resp.json()
    #user sent 2 and shared 2 messages, num messages sent should be 4
    assert r['user_stats']['messages_sent'][-1]['num_messages_sent'] == 4

def test_standup_send():
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
        'length': 1,
    })

    requests.post(config.url + 'standup/send/v1', json={
        'token': payload1['token'],
        'channel_id': payload2['channel_id'],
        'message': 'Message1',
    })

    requests.post(config.url + 'standup/send/v1', json={
        'token': payload1['token'],
        'channel_id': payload2['channel_id'],
        'message': 'Message2',
    })

    requests.post(config.url + 'standup/send/v1', json={
        'token': payload1['token'],
        'channel_id': payload2['channel_id'],
        'message': 'Message3',
    })

    time.sleep(1)

    #get user stats
    resp = requests.get(config.url + 'user/stats/v1', params={'token': payload1['token']})
    r = resp.json()
    #user sent 3 messages
    assert r['user_stats']['messages_sent'][-1]['num_messages_sent'] == 1

def test_message_send_later():
    requests.delete(config.url + 'clear/v1')

    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()

    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_token['token'], 
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id = channel.json()

    resp = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'message': "hello",
        'time_sent': int(datetime.now().timestamp()) + 1,
        'is_pinned': False,
        'reacts':[
                {
                    'react_id': 1,
                    'u_ids': [], 
                    'is_this_user_reacted': False
                }
            ]
    })

    requests.post(config.url + 'message/sendlater/v1', json={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'message': "hello",
        'time_sent': int(datetime.now().timestamp()) + 1,
        'is_pinned': False,
        'reacts':[
                {
                    'react_id': 1,
                    'u_ids': [], 
                    'is_this_user_reacted': False
                }
            ]
    })

    time.sleep(1) 

    #get user stats
    resp = requests.get(config.url + 'user/stats/v1', params={'token': user_token['token']})
    r = resp.json()
    #user sent 3 messages
    assert r['user_stats']['messages_sent'][-1]['num_messages_sent'] == 2


#check correct dms_joined
def test_message_sendlaterdm():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #Register threeusers
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'valid1email@gmail.com', 'password': '123abc!@#', 'name_first': 'Becky', 'name_last': 'Smile'})
    user1_token = user1.json()
    user2_token = user2.json()
    #create a dm
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user1_token['token'],
        'u_ids': [user2_token['auth_user_id']],
    })

    dm_reg = dm.json()
    #send two messages

    requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user1_token['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
        'time_sent': int(datetime.now().timestamp()) + 1,
        'is_pinned': False,
        'reacts':[
                {
                    'react_id': 1,
                    'u_ids': [], 
                    'is_this_user_reacted': False
                }
            ]
    })

    requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user1_token['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
        'time_sent': int(datetime.now().timestamp()) + 1,
        'is_pinned': False,
        'reacts':[
                {
                    'react_id': 1,
                    'u_ids': [], 
                    'is_this_user_reacted': False
                }
            ]
    })


    time.sleep(1)

    #get user stats
    resp = requests.get(config.url + 'user/stats/v1', params={'token':  user1_token['token']})
    r = resp.json()
    #check user sent two messages
    assert r['user_stats']['messages_sent'][-1]['num_messages_sent'] == 2