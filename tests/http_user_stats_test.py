import pytest
import requests
import json
from src import config
import jwt


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
    #assert r2['user_stats']['involvement_rate'] == float(1)
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
def test_correct_messages_sent():
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


#test correct output of whole dictionary

