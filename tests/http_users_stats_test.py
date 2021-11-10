import pytest
import requests
import json
from src import config
import jwt
import time
from datetime import datetime



#check stats are 0 when streams owner first registers
def test_initalise_stats():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #get token from auth reg
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    resp = requests.get(config.url + 'users/stats/v1', params={'token': user_token['token']})
    r = resp.json()
    assert r['workspace_stats']['channels_exist'][0]['num_channels_exist'] == 0
    assert r['workspace_stats']['dms_exist'][0]['num_dms_exist'] == 0
    assert r['workspace_stats']['messages_exist'][0]['num_messages_exist'] == 0

def test_correct_utilization_rate():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #Register three users
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'valid1email@gmail.com', 'password': '123abc!@#', 'name_first': 'Becky', 'name_last': 'Smile'})
    requests.post(config.url + 'auth/register/v2', json={'email': 'valid2email@gmail.com', 'password': '123abc!@#', 'name_first': 'George', 'name_last': 'Peach'})
    user1_token = user1.json()
    user2_token = user2.json()
    #create a channel
    channel1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel1_id = channel1.json() 
    #user 1 join a channel
    requests.post(config.url + 'channel/join/v2', json={'token': user1_token['token'], 'channel_id': channel1_id['channel_id']})
    #user1 and user_2 join dm
    requests.post(config.url + 'dm/create/v1', json={
        'token': user1_token['token'],
        'u_ids': [user2_token['auth_user_id']],
    })
    #get users stats
    resp = requests.get(config.url + 'users/stats/v1', params={'token': user1_token['token']})
    r = resp.json()
    #rate = 2 users joined atleast one channel/dm / 3 users
    assert r['workspace_stats']['utilization_rate'] == float(2/3)

def test_correct_channels_exist():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #Register one users
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create three channels
    requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Snow', 'is_public': True})
    requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Bean', 'is_public': True})
    #get users stats
    resp = requests.get(config.url + 'users/stats/v1', params={'token': user_token['token']})
    r = resp.json()
    #assert latest record is 3 channels
    assert r['workspace_stats']['channels_exist'][-1]['num_channels_exist'] == 3

def test_correct_dms_exist():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #Register three users
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'valid1email@gmail.com', 'password': '123abc!@#', 'name_first': 'Becky', 'name_last': 'Smile'})
    user3 = requests.post(config.url + 'auth/register/v2', json={'email': 'valid2email@gmail.com', 'password': '123abc!@#', 'name_first': 'George', 'name_last': 'Peach'})
    user1_token = user1.json()
    user2_token = user2.json()
    user3_token = user3.json()
    #create three dms
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user1_token['token'],
        'u_ids': [user2_token['auth_user_id']],
    })
    requests.post(config.url + 'dm/create/v1', json={
        'token': user1_token['token'],
        'u_ids': [user3_token['auth_user_id']],
    })
    requests.post(config.url + 'dm/create/v1', json={
        'token': user2_token['token'],
        'u_ids': [user3_token['auth_user_id']],
    })
    dm_reg = dm.json()

    #remove one dm
    requests.delete(config.url + 'dm/remove/v1', json={
        'token': user1_token['token'],
        'dm_id': dm_reg['dm_id'],
    })
    #get users stats
    resp = requests.get(config.url + 'users/stats/v1', params={'token': user1_token['token']})
    r = resp.json()
    #assert latest record is 2 dms
    assert r['workspace_stats']['dms_exist'][-1]['num_dms_exist'] == 2


def test_correct_messages_exist():
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
    resp = requests.get(config.url + 'users/stats/v1', params={'token': user1_token['token']})
    r = resp.json()
    #sent two msgs, removed a msg so total msgs is now 1
    assert r['workspace_stats']['messages_exist'][-1]['num_messages_exist'] == 1

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
    resp = requests.get(config.url + 'users/stats/v1', params={'token': payload1['token']})
    r = resp.json()
    #sent two messages, shared two messages, num_messages_exist should be 4
    assert r['workspace_stats']['messages_exist'][-1]['num_messages_exist'] == 4



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
    resp = requests.get(config.url + 'users/stats/v1', params={'token': payload1['token']})
    r = resp.json()
    #sent three messages, num_messages_exist should be 3
    assert r['workspace_stats']['messages_exist'][-1]['num_messages_exist'] == 1

#test users stats utilization rate is correct after removing user
def test_user_removed():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #Register three users
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'valid1email@gmail.com', 'password': '123abc!@#', 'name_first': 'Becky', 'name_last': 'Smile'})
    requests.post(config.url + 'auth/register/v2', json={'email': 'valid2email@gmail.com', 'password': '123abc!@#', 'name_first': 'George', 'name_last': 'Peach'})
    user1_token = user1.json()
    user2_token = user2.json()
    #create a channel
    requests.post(config.url + 'channels/create/v2', json={'token': user1_token['token'], 'name': 'Alpaca', 'is_public': True})
    #user1 and user_2 join dm
    requests.post(config.url + 'dm/create/v1', json={
        'token': user1_token['token'],
        'u_ids': [user2_token['auth_user_id']],
    })
    #remove the second user
    requests.delete(config.url + 'admin/user/remove/v1', json={'token': user1_token['token'], 'u_id':user2_token['auth_user_id']})
    #get users stats
    resp = requests.get(config.url + 'users/stats/v1', params={'token': user1_token['token']})
    r = resp.json()
    #rate = 2 users joined atleast one channel/dm (but then one got removed so now one userjoined atleast one channel/dm)/ 3 users (then after removal 2 users) = 1/2
    assert r['workspace_stats']['utilization_rate'] == float(1/2)
   
#check dm remove decrements number of existing messages
def test_dm_remove():
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
    dm1 = requests.post(config.url + 'dm/create/v1', json={
        'token': user1_token['token'],
        'u_ids': [user2_token['auth_user_id']],
    })
    first_dm = dm1.json()
    dm2 = requests.post(config.url + 'dm/create/v1', json={
        'token': user1_token['token'],
        'u_ids': [user3_token['auth_user_id']],
    })
    second_dm = dm2.json()
    #send a message in the first dm
    requests.post(config.url + 'message/senddm/v1', json={
        'token': user1_token['token'], 
        'dm_id': first_dm['dm_id'],
        'message': "hello",
    })

    #send three messages in the second dm
    requests.post(config.url + 'message/senddm/v1', json={
        'token': user1_token['token'], 
        'dm_id': second_dm['dm_id'],
        'message': "hello",
    })
    requests.post(config.url + 'message/senddm/v1', json={
        'token': user1_token['token'], 
        'dm_id': second_dm['dm_id'],
        'message': "hello",
    })
    requests.post(config.url + 'message/senddm/v1', json={
        'token': user1_token['token'], 
        'dm_id': second_dm['dm_id'],
        'message': "hello",
    })

    #get user stats
    resp = requests.get(config.url + 'users/stats/v1', params={'token': user1_token['token']})
    r = resp.json()
    #sent four messages
    assert r['workspace_stats']['messages_exist'][-1]['num_messages_exist'] == 4

    #now remove the second dm, which should also decrement the number of messages by three
    requests.delete(config.url + 'dm/remove/v1', json={
        'token': user1_token['token'],
        'dm_id': second_dm ['dm_id'],
    })

    #get user stats
    resp = requests.get(config.url + 'users/stats/v1', params={'token': user1_token['token']})
    r = resp.json()
    #existing messages should now be one
    assert r['workspace_stats']['messages_exist'][-1]['num_messages_exist'] == 1

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
    resp = requests.get(config.url + 'users/stats/v1', params={'token': user_token['token']})
    r = resp.json()

    assert r['workspace_stats']['messages_exist'][-1]['num_messages_exist'] == 2

#check correct dms_joined
def test_message_sendlaterdm():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #Register two users
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'valid1email@gmail.com', 'password': '123abc!@#', 'name_first': 'Becky', 'name_last': 'Smile'})
    user1_token = user1.json()
    user2_token = user2.json()
    #create one dms
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

    time.sleep(1)

    #get users  stats
    resp = requests.get(config.url + 'users/stats/v1', params={'token': user2_token['token']})
    r = resp.json()

    assert r['workspace_stats']['messages_exist'][-1]['num_messages_exist'] == 1

def test_sendlaterdm_work():
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

    requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user_token['token'], 
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
    'token': user_token['token'], 
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
    resp = requests.get(config.url + 'users/stats/v1', params={'token': user_token['token']})
    r = resp.json()

    assert r['workspace_stats']['messages_exist'][-1]['num_messages_exist'] == 2
